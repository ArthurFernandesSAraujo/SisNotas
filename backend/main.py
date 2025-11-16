import tkinter as tk
from tkinter import messagebox
from init_db import inicializar_banco
from db import conectar_bd, fechar_bd
import secretaria
import professor
import aluno  

# Inicializa o banco ao abrir o programa
inicializar_banco()

# =======================================================
# FUNÇÃO PRINCIPAL DO LOGIN  → PERMITE VOLTAR PARA O LOGIN
# =======================================================
def janela_login():
    janela = tk.Tk()
    janela.title("Login - Sistema Escolar")
    janela.geometry("330x300")
    janela.resizable(False, False)

    # ==========================
    # CAMPOS DE LOGIN
    # ==========================
    tk.Label(janela, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(janela)
    entry_usuario.pack(pady=5)

    tk.Label(janela, text="Senha:").pack(pady=5)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack(pady=5)

    # ==========================
    # SELEÇÃO DO TIPO DE USUÁRIO
    # ==========================
    tk.Label(janela, text="Entrar como:").pack(pady=5)
    tipo_var = tk.StringVar(value="Selecione")

    opcoes = ["secretaria", "professor", "aluno"]
    tk.OptionMenu(janela, tipo_var, *opcoes).pack(pady=5)

    # ==========================
    # FUNÇÃO DE LOGIN
    # ==========================
    def validar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        tipo_selecionado = tipo_var.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        if tipo_selecionado == "Selecione":
            messagebox.showwarning("Atenção", "Escolha o tipo de usuário!")
            return

        con, cur = conectar_bd()
        if not con:
            messagebox.showerror("Erro", "Falha ao conectar ao banco.")
            return

        try:
            cur.execute("SELECT * FROM usuarios WHERE username=%s AND senha=%s", (usuario, senha))
            user = cur.fetchone()

            if user:
                nivel = user['nivel']

                # impede login incorreto
                if nivel != tipo_selecionado:
                    messagebox.showerror("Erro", "Tipo de usuário incorreto!")
                    return

                messagebox.showinfo("Bem-vindo", f"{user['nome']} ({user['nivel']})")

                janela.destroy()

                # abre painéis corretos
                if nivel == "secretaria":
                    secretaria.abrir_tela_secretaria()

                elif nivel == "professor":
                    professor.abrir_tela_professor(user['nome'])

                elif nivel == "aluno":
                    aluno.abrir_tela_aluno(user['nome'])

            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos!")

        except Exception as e:
            messagebox.showerror("Erro BD", str(e))
        finally:
            fechar_bd(con, cur)

    # BOTÃO DE ENTRAR
    tk.Button(
        janela,
        text="Entrar",
        bg="#0E4D92",
        fg="white",
        width=15,
        command=validar_login
    ).pack(pady=15)

    janela.mainloop()


# =======================================================
# INICIA PROGRAMA NO LOGIN
# =======================================================
if __name__ == "__main__":
    janela_login()
