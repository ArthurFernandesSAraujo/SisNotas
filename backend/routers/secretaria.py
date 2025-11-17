from fastapi import APIRouter, HTTPException
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/secretaria", tags=["Secretaria / Admin"])


# =============================================================
# 1) CRUD PROFESSORES
# =============================================================

@router.get("/professores")
def listar_professores():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM professores")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/professores")
def cadastrar_professor(nome: str, email: str):
    con, cur = conectar_bd()
    cur.execute("INSERT INTO professores (nome, email) VALUES (%s, %s)", (nome, email))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor cadastrado com sucesso"}

@router.put("/professores/{idprofessor}")
def atualizar_professor(idprofessor: int, nome: str, email: str):
    con, cur = conectar_bd()
    cur.execute("UPDATE professores SET nome=%s, email=%s WHERE idprofessor=%s",
                (nome, email, idprofessor))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor atualizado com sucesso"}

@router.delete("/professores/{idprofessor}")
def excluir_professor(idprofessor: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM professores WHERE idprofessor=%s", (idprofessor,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor excluído com sucesso"}


# =============================================================
# 2) CRUD ALUNOS
# =============================================================

@router.get("/alunos")
def listar_alunos():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM alunos")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/alunos")
def cadastrar_aluno(nome: str, matricula: str, email: str):
    con, cur = conectar_bd()
    cur.execute(
        "INSERT INTO alunos (nome, matricula, email) VALUES (%s, %s, %s)",
        (nome, matricula, email)
    )
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno cadastrado com sucesso"}

@router.put("/alunos/{idaluno}")
def atualizar_aluno(idaluno: int, nome: str, matricula: str, email: str):
    con, cur = conectar_bd()
    cur.execute(
        "UPDATE alunos SET nome=%s, matricula=%s, email=%s WHERE idaluno=%s",
        (nome, matricula, email, idaluno)
    )
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno atualizado com sucesso"}

@router.delete("/alunos/{idaluno}")
def excluir_aluno(idaluno: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM alunos WHERE idaluno=%s", (idaluno,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno excluído com sucesso"}


# =============================================================
# 3) CRUD MATÉRIAS
# =============================================================

@router.get("/materias")
def listar_materias():
    con, cur = conectar_bd()
    cur.execute("""
        SELECT m.*, p.nome AS professor
        FROM materias m
        LEFT JOIN professores p ON m.idprofessor = p.idprofessor
    """)
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/materias")
def cadastrar_materia(nome: str):
    con, cur = conectar_bd()
    cur.execute("INSERT INTO materias (nome) VALUES (%s)", (nome,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria cadastrada com sucesso"}

@router.put("/materias/{idmateria}")
def atualizar_materia(idmateria: int, nome: str):
    con, cur = conectar_bd()
    cur.execute("UPDATE materias SET nome=%s WHERE idmateria=%s", (nome, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria atualizada com sucesso"}

@router.delete("/materias/{idmateria}")
def excluir_materia(idmateria: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM materias WHERE idmateria=%s", (idmateria,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria excluída com sucesso"}


# =============================================================
# 4) NOTAS — Secretaria pode fazer tudo
# =============================================================

@router.get("/notas")
def listar_notas():
    con, cur = conectar_bd()
    cur.execute("""
        SELECT n.idnota, a.nome AS aluno, m.nome AS materia, p.nome AS professor, n.nota
        FROM notas n
        JOIN alunos a ON n.idaluno = a.idaluno
        JOIN materias m ON n.idmateria = m.idmateria
        JOIN professores p ON n.idprofessor = p.idprofessor
    """)
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/notas")
def lançar_nota(idaluno: int, idmateria: int, idprofessor: int, nota: float):
    con, cur = conectar_bd()
    cur.execute("""
        INSERT INTO notas (idaluno, idmateria, idprofessor, nota)
        VALUES (%s, %s, %s, %s)
    """, (idaluno, idmateria, idprofessor, nota))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota lançada com sucesso"}

@router.put("/notas/{idnota}")
def atualizar_nota(idnota: int, nota: float):
    con, cur = conectar_bd()
    cur.execute("UPDATE notas SET nota=%s WHERE idnota=%s", (nota, idnota))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota atualizada com sucesso"}

@router.delete("/notas/{idnota}")
def excluir_nota(idnota: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM notas WHERE idnota=%s", (idnota,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota excluída com sucesso"}


# =============================================================
# 5) ASSOCIAÇÕES
# =============================================================

@router.post("/associar/aluno-materia")
def associar_aluno_materia(idaluno: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute("INSERT IGNORE INTO aluno_materias (idaluno, idmateria) VALUES (%s, %s)",
                (idaluno, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno associado à matéria"}

@router.post("/associar/professor-materia")
def associar_professor_materia(idprofessor: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute(
        "UPDATE materias SET idprofessor=%s WHERE idmateria=%s",
        (idprofessor, idmateria)
    )
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor associado à matéria"}
