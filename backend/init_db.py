import mysql.connector

config = {
    "host": "localhost",
    "user": "root",
    "password": ""
}

def inicializar_banco():
    try:
        con = mysql.connector.connect(**config)
        cur = con.cursor()

        # Criar banco
        cur.execute("CREATE DATABASE IF NOT EXISTS escola;")
        print(" Banco 'escola' verificado/criado.")

        cur.execute("USE escola;")

        # ======== TABELAS DO MODELO CORRETO ========
        tabelas = [

            # -------------------------
            # Usuários (Login do sistema)
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                idusuarios INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                senha VARCHAR(100) NOT NULL,
                nivel ENUM('secretaria', 'professor', 'aluno') NOT NULL
            );
            """,

            # -------------------------
            # Professores
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS professores (
                idprofessor INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100)
            );
            """,

            # -------------------------
            # Matérias (agora sem professor obrigatório)
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS materias (
                idmateria INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                idprofessor INT NULL,
                FOREIGN KEY (idprofessor) REFERENCES professores(idprofessor)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
            """,

            # -------------------------
            # Alunos
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS alunos (
                idaluno INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                matricula VARCHAR(20) UNIQUE NOT NULL,
                email VARCHAR(100)
            );
            """,

            # -------------------------
            # Aluno x Matéria (N:N)
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS aluno_materias (
                idaluno INT NOT NULL,
                idmateria INT NOT NULL,
                PRIMARY KEY (idaluno, idmateria),
                FOREIGN KEY (idaluno) REFERENCES alunos(idaluno)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                FOREIGN KEY (idmateria) REFERENCES materias(idmateria)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """,

            # -------------------------
            # Notas (Aluno + Matéria + Professor)
            # -------------------------
            """
            CREATE TABLE IF NOT EXISTS notas (
                idnota INT AUTO_INCREMENT PRIMARY KEY,
                idaluno INT NOT NULL,
                idmateria INT NOT NULL,
                idprofessor INT NOT NULL,
                nota DECIMAL(4,2),

                FOREIGN KEY (idaluno) REFERENCES alunos(idaluno)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,

                FOREIGN KEY (idmateria) REFERENCES materias(idmateria)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,

                FOREIGN KEY (idprofessor) REFERENCES professores(idprofessor)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        ]

        # Criar tabelas
        for sql in tabelas:
            cur.execute(sql)

        print(" Tabelas criadas/verificadas com sucesso.")

        # Criar usuários iniciais (se vazio)
        cur.execute("SELECT COUNT(*) FROM usuarios;")
        qtd = cur.fetchone()[0]

        if qtd == 0:
            cur.executemany("""
                INSERT INTO usuarios (nome, username, senha, nivel)
                VALUES (%s, %s, %s, %s)
            """, [
                ('Maria Secretaria', 'maria', '123', 'secretaria'),
                ('João Professor', 'joao', '123', 'professor'),
                ('Ana Aluna', 'ana', '123', 'aluno')
            ])
            con.commit()
            print(" Usuários iniciais criados.")
        else:
            print(" Usuários já existentes, sem necessidade de recriar.")

        cur.close()
        con.close()
        print("🚀 Banco pronto para uso!")

    except mysql.connector.Error as e:
        print("❌ Erro ao inicializar o banco:", e)

if __name__ == "__main__":
    inicializar_banco()
