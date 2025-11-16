import tkinter as tk
from tkinter import messagebox
from db import conectar_bd, fechar_bd
from main import janela_login  


def abrir_tela_secretaria():
    janela = tk.Tk()
    janela.title("Painel da Secretaria")
    janela.geometry("1000x650")

    menu = tk.Frame(janela, width=240, bg="#0E4D92")
    menu.pack(side="left", fill="y")

    conteudo = tk.Frame(janela, bg="white")
    conteudo.pack(side="right", fill="both", expand=True)

    def limpar_conteudo():
        for widget in conteudo.winfo_children():
            widget.destroy()

    # ============================================================
    # 1 — CADASTRAR PROFESSOR
    # ============================================================
    def cadastrar_professor():
        limpar_conteudo()
        tk.Label(conteudo, text="Cadastrar Professor", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(conteudo, text="Nome:").pack()
        nome_entry = tk.Entry(conteudo, width=40)
        nome_entry.pack()

        tk.Label(conteudo, text="E-mail:").pack()
        email_entry = tk.Entry(conteudo, width=40)
        email_entry.pack()

        tk.Label(conteudo, text="Usuário (login):").pack()
        username_entry = tk.Entry(conteudo, width=40)
        username_entry.pack()

        tk.Label(conteudo, text="Senha:").pack()
        senha_entry = tk.Entry(conteudo, width=40, show="*")
        senha_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()
            email = email_entry.get().strip()
            username = username_entry.get().strip()
            senha = senha_entry.get().strip()

            if not nome or not username or not senha:
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
                return

            con, cur = conectar_bd()
            try:
                cur.execute("INSERT INTO professores (nome, email) VALUES (%s, %s)", (nome, email))
                con.commit()

                cur.execute(
                    "INSERT INTO usuarios (nome, username, senha, nivel) VALUES (%s, %s, %s, 'professor')",
                    (nome, username, senha)
                )
                con.commit()

                messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")

                nome_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                username_entry.delete(0, tk.END)
                senha_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                fechar_bd(con, cur)

        tk.Button(conteudo, text="Salvar", bg="#0E4D92", fg="white", command=salvar).pack(pady=15)

    # ============================================================
    # 2 — CADASTRAR MATÉRIA
    # ============================================================
    def cadastrar_materia():
        limpar_conteudo()
        tk.Label(conteudo, text="Cadastrar Matéria", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(conteudo, text="Nome da Matéria:").pack()
        nome_entry = tk.Entry(conteudo, width=40)
        nome_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()

            if not nome:
                messagebox.showwarning("Atenção", "Informe o nome da matéria.")
                return

            con, cur = conectar_bd()
            try:
                cur.execute("INSERT INTO materias (nome) VALUES (%s)", (nome,))
                con.commit()

                messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
                nome_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                fechar_bd(con, cur)

        tk.Button(conteudo, text="Salvar Matéria", bg="#0E4D92", fg="white", command=salvar).pack(pady=15)

    # ============================================================
    # 3 — CADASTRAR ALUNO
    # ============================================================
    def cadastrar_aluno():
        limpar_conteudo()
        tk.Label(conteudo, text="Cadastrar Aluno", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(conteudo, text="Nome:").pack()
        nome_entry = tk.Entry(conteudo, width=40)
        nome_entry.pack()

        tk.Label(conteudo, text="Matrícula:").pack()
        matricula_entry = tk.Entry(conteudo, width=40)
        matricula_entry.pack()

        tk.Label(conteudo, text="E-mail:").pack()
        email_entry = tk.Entry(conteudo, width=40)
        email_entry.pack()

        tk.Label(conteudo, text="Usuário (login):").pack()
        username_entry = tk.Entry(conteudo, width=40)
        username_entry.pack()

        tk.Label(conteudo, text="Senha:").pack()
        senha_entry = tk.Entry(conteudo, width=40, show="*")
        senha_entry.pack()

        def salvar():
            nome = nome_entry.get().strip()
            matricula = matricula_entry.get().strip()
            email = email_entry.get().strip()
            username = username_entry.get().strip()
            senha = senha_entry.get().strip()

            if not nome or not matricula or not username or not senha:
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
                return

            con, cur = conectar_bd()
            try:
                cur.execute(
                    "INSERT INTO alunos (nome, matricula, email) VALUES (%s, %s, %s)",
                    (nome, matricula, email)
                )
                con.commit()

                cur.execute(
                    "INSERT INTO usuarios (nome, username, senha, nivel) VALUES (%s, %s, %s, 'aluno')",
                    (nome, username, senha)
                )
                con.commit()

                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                fechar_bd(con, cur)

        tk.Button(conteudo, text="Salvar Aluno", bg="#0E4D92", fg="white", command=salvar).pack(pady=15)

    # ============================================================
    # 4 — MATRICULAR ALUNO EM MATÉRIA
    # ============================================================
    def associar_aluno_materia():
        limpar_conteudo()
        tk.Label(conteudo, text="Associar Aluno a Matérias", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(conteudo, text="Selecione o Aluno:").pack()
        aluno_var = tk.StringVar(value="Selecione")
        aluno_menu = tk.OptionMenu(conteudo, aluno_var, "")
        aluno_menu.pack()

        con, cur = conectar_bd()
        cur.execute("SELECT idaluno, nome FROM alunos ORDER BY nome")
        alunos = cur.fetchall()
        aluno_menu["menu"].delete(0, "end")
        for a in alunos:
            texto = f"{a['idaluno']} - {a['nome']}"
            aluno_menu["menu"].add_command(label=texto, command=lambda v=texto: aluno_var.set(v))
        fechar_bd(con, cur)

        tk.Label(conteudo, text="Selecione a Matéria:").pack()
        materia_var = tk.StringVar(value="Selecione")
        materia_menu = tk.OptionMenu(conteudo, materia_var, "")
        materia_menu.pack()

        con, cur = conectar_bd()
        cur.execute("SELECT idmateria, nome FROM materias ORDER BY nome")
        materias = cur.fetchall()
        fechar_bd(con, cur)

        materia_menu["menu"].delete(0, "end")
        for m in materias:
            texto = f"{m['idmateria']} - {m['nome']}"
            materia_menu["menu"].add_command(label=texto, command=lambda v=texto: materia_var.set(v))

        def salvar():
            if aluno_var.get() == "Selecione" or materia_var.get() == "Selecione":
                messagebox.showwarning("Atenção", "Selecione aluno e matéria.")
                return

            idaluno = aluno_var.get().split(" - ")[0]
            idmateria = materia_var.get().split(" - ")[0]

            con, cur = conectar_bd()
            try:
                cur.execute("INSERT IGNORE INTO aluno_materias (idaluno, idmateria) VALUES (%s, %s)",
                            (idaluno, idmateria))
                con.commit()
                messagebox.showinfo("Sucesso", "Aluno matriculado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                fechar_bd(con, cur)

        tk.Button(conteudo, text="Salvar Associação", bg="#0E4D92", fg="white", command=salvar).pack(pady=15)

    # ============================================================
    # 5 — ASSOCIAR PROFESSOR A MATÉRIA
    # ============================================================
    def associar_professor_materia():
        limpar_conteudo()
        tk.Label(conteudo, text="Associar Professor a Matéria", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(conteudo, text="Selecione o Professor:").pack()
        prof_var = tk.StringVar(value="Selecione")
        prof_menu = tk.OptionMenu(conteudo, prof_var, "")
        prof_menu.pack()

        con, cur = conectar_bd()
        cur.execute("SELECT idprofessor, nome FROM professores ORDER BY nome")
        profs = cur.fetchall()
        fechar_bd(con, cur)

        prof_menu["menu"].delete(0, "end")
        for p in profs:
            texto = f"{p['idprofessor']} - {p['nome']}"
            prof_menu["menu"].add_command(label=texto, command=lambda v=texto: prof_var.set(v))

        tk.Label(conteudo, text="Selecione a Matéria:").pack()
        mat_var = tk.StringVar(value="Selecione")
        mat_menu = tk.OptionMenu(conteudo, mat_var, "")
        mat_menu.pack()

        con, cur = conectar_bd()
        cur.execute("SELECT idmateria, nome FROM materias ORDER BY nome")
        mats = cur.fetchall()
        fechar_bd(con, cur)

        mat_menu["menu"].delete(0, "end")
        for m in mats:
            texto = f"{m['idmateria']} - {m['nome']}"
            mat_menu["menu"].add_command(label=texto, command=lambda v=texto: mat_var.set(v))

        def salvar():
            if prof_var.get() == "Selecione" or mat_var.get() == "Selecione":
                messagebox.showwarning("Atenção", "Selecione professor e matéria.")
                return

            idprof = prof_var.get().split(" - ")[0]
            idmateria = mat_var.get().split(" - ")[0]

            con, cur = conectar_bd()
            try:
                cur.execute("UPDATE materias SET idprofessor=%s WHERE idmateria=%s",
                            (idprof, idmateria))
                con.commit()
                messagebox.showinfo("Sucesso", "Professor associado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
            finally:
                fechar_bd(con, cur)

        tk.Button(conteudo, text="Salvar Associação", bg="#0E4D92", fg="white", command=salvar).pack(pady=15)

    # ============================================================
    # 6 — LISTAR PROFESSORES
    # ============================================================
    def listar_professores():
        limpar_conteudo()
        tk.Label(conteudo, text="Professores e suas Matérias", font=("Arial", 18, "bold")).pack(pady=10)

        lista = tk.Listbox(conteudo, width=100, height=15)
        lista.pack(pady=10)

        con, cur = conectar_bd()
        cur.execute("""
            SELECT p.nome AS professor, m.nome AS materia
            FROM professores p
            LEFT JOIN materias m ON p.idprofessor = m.idprofessor
            ORDER BY p.nome, m.nome
        """)
        dados = cur.fetchall()
        fechar_bd(con, cur)

        atual = None
        for row in dados:
            prof = row['professor']
            mat = row['materia']

            if prof != atual:
                lista.insert(tk.END, f"\nPROFESSOR: {prof}")
                atual = prof

            lista.insert(tk.END, f"   → {mat}")

    # ============================================================
    # 7 — SAIR (VOLTAR PARA O LOGIN)
    # ============================================================
    def sair():
        janela.destroy()
        janela_login()

    # ============================================================
    # MENU LATERAL
    # ============================================================
    botoes = [
        ("Cadastrar Professor", cadastrar_professor),
        ("Cadastrar Matéria", cadastrar_materia),
        ("Cadastrar Aluno", cadastrar_aluno),
        ("Matricular Aluno em Matérias", associar_aluno_materia),
        ("Associar Professor a Matéria", associar_professor_materia),
        ("Listar Professores + Matérias", listar_professores),
        ("Sair", sair)
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
        ).pack(pady=6, padx=10)

    janela.mainloop()
