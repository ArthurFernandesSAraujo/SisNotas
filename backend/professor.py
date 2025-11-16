import tkinter as tk
from tkinter import messagebox
from db import conectar_bd, fechar_bd
import main  

def abrir_tela_professor(professor_nome):
    janela = tk.Tk()
    janela.title(f"Painel do Professor - {professor_nome}")
    janela.geometry("950x650")

    # Buscar ID do professor
    con, cur = conectar_bd()
    cur.execute("SELECT idprofessor FROM professores WHERE nome = %s", (professor_nome,))
    prof = cur.fetchone()
    fechar_bd(con, cur)

    if not prof:
        messagebox.showerror("Erro", "Professor não encontrado!")
        janela.destroy()
        return

    id_professor = prof["idprofessor"]

    # LAYOUT
    menu = tk.Frame(janela, width=240, bg="#2E86C1")
    menu.pack(side="left", fill="y")

    conteudo = tk.Frame(janela, bg="white")
    conteudo.pack(side="right", fill="both", expand=True)

    def limpar():
        for w in conteudo.winfo_children():
            w.destroy()

    # ============================================================
    # 1) VER MATÉRIAS
    # ============================================================
    def ver_materias():
        limpar()
        tk.Label(conteudo, text="Suas Matérias", font=("Arial", 18, "bold")).pack(pady=10)

        lista = tk.Listbox(conteudo, width=90, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT idmateria, nome 
            FROM materias 
            WHERE idprofessor = %s
            ORDER BY nome
        """, (id_professor,))
        materias = cur.fetchall()
        fechar_bd(con, cur)

        if not materias:
            lista.insert(tk.END, "⚠️ Você ainda não está vinculado a nenhuma matéria.")
            return

        for m in materias:
            lista.insert(tk.END, f"{m['idmateria']} - {m['nome']}")

    # ============================================================
    # 2) VER ALUNOS POR MATÉRIA
    # ============================================================
    def alunos_da_materia():
        limpar()
        tk.Label(conteudo, text="Alunos por Matéria", font=("Arial", 18, "bold")).pack(pady=10)

        materia_var = tk.StringVar(value="Selecione")
        materia_menu = tk.OptionMenu(conteudo, materia_var, "")
        materia_menu.pack(pady=5)

        # Carregar matérias
        con, cur = conectar_bd()
        cur.execute("SELECT idmateria, nome FROM materias WHERE idprofessor=%s", (id_professor,))
        materias = cur.fetchall()
        fechar_bd(con, cur)

        materia_menu["menu"].delete(0, "end")
        for m in materias:
            texto = f"{m['idmateria']} - {m['nome']}"
            materia_menu["menu"].add_command(
                label=texto, command=lambda v=texto: materia_var.set(v)
            )

        lista = tk.Listbox(conteudo, width=90, height=15)

        def carregar():
            lista.delete(0, tk.END)

            if materia_var.get() == "Selecione":
                return

            idmateria = materia_var.get().split(" - ")[0]

            con, cur = conectar_bd()
            cur.execute("""
                SELECT a.idaluno, a.nome, a.matricula
                FROM aluno_materias am
                JOIN alunos a ON am.idaluno = a.idaluno
                WHERE am.idmateria = %s
                ORDER BY a.nome
            """, (idmateria,))
            alunos = cur.fetchall()
            fechar_bd(con, cur)

            lista.pack(pady=10)

            if not alunos:
                lista.insert(tk.END, "⚠️ Nenhum aluno matriculado nesta matéria.")
                return

            for a in alunos:
                lista.insert(tk.END, f"{a['idaluno']} - {a['nome']} (Mat: {a['matricula']})")

        tk.Button(conteudo, text="Carregar Alunos", bg="#2E86C1", fg="white",
                  command=carregar).pack(pady=10)

    # ============================================================
    # 3) LANÇAR / ATUALIZAR NOTAS
    # ============================================================
    def lancar_notas():
        limpar()
        tk.Label(conteudo, text="Lançar / Atualizar Notas", font=("Arial", 18, "bold")).pack(pady=10)

        materia_var = tk.StringVar(value="Selecione")
        materia_menu = tk.OptionMenu(conteudo, materia_var, "")
        materia_menu.pack(pady=5)

        con, cur = conectar_bd()
        cur.execute("SELECT idmateria, nome FROM materias WHERE idprofessor=%s", (id_professor,))
        materias = cur.fetchall()
        fechar_bd(con, cur)

        materia_menu["menu"].delete(0, "end")
        for m in materias:
            texto = f"{m['idmateria']} - {m['nome']}"
            materia_menu["menu"].add_command(
                label=texto, command=lambda v=texto: materia_var.set(v)
            )

        lista = tk.Listbox(conteudo, width=90, height=15)

        def carregar():
            lista.delete(0, tk.END)

            if materia_var.get() == "Selecione":
                return

            idmateria = materia_var.get().split(" - ")[0]

            con, cur = conectar_bd()
            cur.execute("""
                SELECT a.idaluno, a.nome, a.matricula
                FROM aluno_materias am
                JOIN alunos a ON am.idaluno = a.idaluno
                WHERE am.idmateria=%s
            """, (idmateria,))
            alunos = cur.fetchall()
            fechar_bd(con, cur)

            lista.pack(pady=10)

            for a in alunos:
                lista.insert(tk.END, f"{a['idaluno']} - {a['nome']} (Mat: {a['matricula']})")

        tk.Button(conteudo, text="Carregar Alunos", bg="#2E86C1", fg="white",
                  command=carregar).pack(pady=8)

        # Entrada da nota
        frame = tk.Frame(conteudo)
        frame.pack(pady=5)
        tk.Label(frame, text="Nota:").grid(row=0, column=0, padx=5)
        entry_nota = tk.Entry(frame, width=10)
        entry_nota.grid(row=0, column=1, padx=5)

        def salvar():
            if not lista.curselection():
                messagebox.showwarning("Atenção", "Selecione um aluno.")
                return

            linha = lista.get(lista.curselection()[0])
            idaluno = linha.split(" - ")[0]
            idmateria = materia_var.get().split(" - ")[0]

            nota = entry_nota.get().strip()

            try:
                v = float(nota)
                if v < 0 or v > 10:
                    raise ValueError
            except:
                messagebox.showwarning("Erro", "Nota inválida.")
                return

            con, cur = conectar_bd()

            cur.execute("""
                SELECT idnota FROM notas 
                WHERE idaluno=%s AND idmateria=%s AND idprofessor=%s
            """, (idaluno, idmateria, id_professor))
            existe = cur.fetchone()

            if existe:
                cur.execute("UPDATE notas SET nota=%s WHERE idnota=%s", (v, existe["idnota"]))
            else:
                cur.execute("""
                    INSERT INTO notas (idaluno, idmateria, idprofessor, nota)
                    VALUES (%s, %s, %s, %s)
                """, (idaluno, idmateria, id_professor, v))

            con.commit()
            fechar_bd(con, cur)
            messagebox.showinfo("Sucesso", "Nota salva!")

        tk.Button(conteudo, text="Salvar Nota", bg="#27AE60", fg="white",
                  command=salvar).pack(pady=10)

    # ============================================================
    # 4) GERENCIAR NOTAS
    # ============================================================
    def gerenciar_notas():
        limpar()
        tk.Label(conteudo, text="Gerenciar Notas", font=("Arial", 18, "bold")).pack(pady=10)

        lista = tk.Listbox(conteudo, width=90, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT n.idnota, m.nome AS materia, a.nome AS aluno, n.nota
            FROM notas n
            JOIN materias m ON n.idmateria = m.idmateria
            JOIN alunos a ON n.idaluno = a.idaluno
            WHERE n.idprofessor = %s
            ORDER BY m.nome, a.nome
        """, (id_professor,))
        notas = cur.fetchall()
        fechar_bd(con, cur)

        if not notas:
            lista.insert(tk.END, "⚠️ Nenhuma nota lançada.")
            return

        for n in notas:
            lista.insert(tk.END, f"{n['idnota']} - {n['materia']} - {n['aluno']} → Nota:{n['nota']}")

        frame = tk.Frame(conteudo)
        frame.pack()

        tk.Label(frame, text="Nova Nota:").grid(row=0, column=0, padx=5)
        entry_nova = tk.Entry(frame, width=10)
        entry_nova.grid(row=0, column=1, padx=5)

        def editar():
            if not lista.curselection():
                messagebox.showwarning("Atenção", "Selecione uma nota.")
                return

            idnota = lista.get(lista.curselection()[0]).split(" - ")[0]
            nova = entry_nova.get().strip()

            try:
                v = float(nova)
                if v < 0 or v > 10:
                    raise ValueError
            except:
                messagebox.showwarning("Erro", "Nota inválida.")
                return

            con, cur = conectar_bd()
            cur.execute("UPDATE notas SET nota=%s WHERE idnota=%s", (v, idnota))
            con.commit()
            fechar_bd(con, cur)
            messagebox.showinfo("Sucesso", "Nota atualizada!")
            gerenciar_notas()

        tk.Button(frame, text="Editar", bg="#27AE60", fg="white",
                  command=editar).grid(row=0, column=2, padx=10)

        def excluir():
            if not lista.curselection():
                messagebox.showwarning("Atenção", "Selecione uma nota.")
                return

            idnota = lista.get(lista.curselection()[0]).split(" - ")[0]

            if not messagebox.askyesno("Confirmação", "Excluir essa nota?"):
                return

            con, cur = conectar_bd()
            cur.execute("DELETE FROM notas WHERE idnota=%s", (idnota,))
            con.commit()
            fechar_bd(con, cur)

            messagebox.showinfo("Sucesso", "Nota excluída!")
            gerenciar_notas()

        tk.Button(frame, text="Excluir", bg="#C0392B", fg="white",
                  command=excluir).grid(row=0, column=3, padx=10)

    # ============================================================
    # 5) SAIR (VOLTAR PARA LOGIN)
    # ============================================================
    def sair():
        janela.destroy()
        main.janela_login()

    # ============================================================
    # MENU LATERAL
    # ============================================================
    botoes = [
        ("Ver Minhas Matérias", ver_materias),
        ("Alunos por Matéria", alunos_da_materia),
        ("Lançar Notas", lancar_notas),
        ("Gerenciar Notas", gerenciar_notas),
        ("Sair", sair)
    ]

    for texto, comando in botoes:
        tk.Button(menu, text=texto, bg="#2E86C1", fg="white",
                  width=25, anchor="w", command=comando).pack(pady=8)

    janela.mainloop()
