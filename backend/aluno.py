import tkinter as tk
from tkinter import messagebox
from db import conectar_bd, fechar_bd
import main  

def abrir_tela_aluno(nome_aluno):
    """Tela principal do aluno com seções separadas"""
    janela = tk.Tk()
    janela.title(f"Painel do Aluno - {nome_aluno}")
    janela.geometry("900x550")
    janela.config(bg="white")

    # ================================
    # PAINEL LATERAL
    # ================================
    menu = tk.Frame(janela, width=220, bg="#0E4D92")
    menu.pack(side="left", fill="y")

    conteudo = tk.Frame(janela, bg="white")
    conteudo.pack(side="right", fill="both", expand=True)

    def limpar_conteudo():
        for widget in conteudo.winfo_children():
            widget.destroy()

    # ================================
    # Buscar ID do aluno
    # ================================
    con, cur = conectar_bd()
    cur.execute("SELECT idaluno FROM alunos WHERE nome = %s", (nome_aluno,))
    aluno = cur.fetchone()
    fechar_bd(con, cur)

    if not aluno:
        messagebox.showerror("Erro", "Aluno não encontrado!")
        janela.destroy()
        return

    idaluno = aluno["idaluno"]

    # ===========================================================
    # 1️⃣ SEÇÃO — MINHAS MATÉRIAS
    # ===========================================================
    def ver_materias():
        limpar_conteudo()
        tk.Label(conteudo, text="📘 Minhas Matérias", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        lista = tk.Listbox(conteudo, width=80, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT m.nome AS materia
            FROM aluno_materias am
            JOIN materias m ON am.idmateria = m.idmateria
            WHERE am.idaluno = %s
            ORDER BY m.nome
        """, (idaluno,))
        materias = cur.fetchall()
        fechar_bd(con, cur)

        if not materias:
            lista.insert(tk.END, "⚠️ Você não está matriculado em nenhuma matéria.")
        else:
            for m in materias:
                lista.insert(tk.END, f"- {m['materia']}")

    # ===========================================================
    # 2️⃣ SEÇÃO — MINHAS NOTAS
    # ===========================================================
    def ver_notas():
        limpar_conteudo()
        tk.Label(conteudo, text="📝 Minhas Notas", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        lista = tk.Listbox(conteudo, width=80, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT m.nome AS materia, n.nota
            FROM notas n
            JOIN materias m ON n.idmateria = m.idmateria
            WHERE n.idaluno = %s
            ORDER BY m.nome
        """, (idaluno,))
        notas = cur.fetchall()
        fechar_bd(con, cur)

        if not notas:
            lista.insert(tk.END, "⚠️ Nenhuma nota lançada ainda.")
        else:
            for n in notas:
                lista.insert(tk.END, f"{n['materia']}: {n['nota']}")

    # ===========================================================
    # 3️⃣ SEÇÃO — MEUS PROFESSORES
    # ===========================================================
    def ver_professores():
        limpar_conteudo()
        tk.Label(conteudo, text="👨‍🏫 Meus Professores", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        lista = tk.Listbox(conteudo, width=80, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT m.nome AS materia, p.nome AS professor
            FROM aluno_materias am
            JOIN materias m ON am.idmateria = m.idmateria
            JOIN professores p ON m.idprofessor = p.idprofessor
            WHERE am.idaluno = %s
            ORDER BY m.nome
        """, (idaluno,))
        professores = cur.fetchall()
        fechar_bd(con, cur)

        if not professores:
            lista.insert(tk.END, "⚠️ Você não está matriculado em nenhuma matéria.")
        else:
            for p in professores:
                lista.insert(tk.END, f"{p['materia']} → Prof. {p['professor']}")

    # ===========================================================
    # BOTÃO SAIR — VOLTAR PARA LOGIN
    # ===========================================================
    def voltar_login():
        janela.destroy()
        main.janela_login()  # chama a função do login

    # ================================
    # BOTÕES DO MENU
    # ================================
    botoes = [
        ("📘 Minhas Matérias", ver_materias),
        ("📝 Minhas Notas", ver_notas),
        ("👨‍🏫 Meus Professores", ver_professores),
        ("🚪 Sair", voltar_login)
    ]

    for texto, comando in botoes:
        tk.Button(
            menu,
            text=texto,
            bg="#0E4D92",
            fg="white",
            width=25,
            anchor="w",
            command=comando
        ).pack(pady=8, padx=10)

    janela.mainloop()
