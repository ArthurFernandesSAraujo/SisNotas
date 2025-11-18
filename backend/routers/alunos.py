from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/")
def listar_alunos():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM alunos")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/")
def cadastrar_aluno(nome: str, matricula: str, email: str):
    con, cur = conectar_bd()
    cur.execute("""
        INSERT INTO alunos (nome, matricula, email) VALUES (%s, %s, %s)
    """, (nome, matricula, email))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno cadastrado!"}

@router.get("/{idaluno}/materias")
def materias_do_aluno(idaluno: int):
    con, cur = conectar_bd()
    cur.execute("""
        SELECT m.nome FROM aluno_materias am
        JOIN materias m ON am.idmateria = m.idmateria
        WHERE am.idaluno=%s
    """, (idaluno,))
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.get("/{idaluno}/notas")
def notas_do_aluno(idaluno: int):
    con, cur = conectar_bd()
    cur.execute("""
        SELECT m.nome AS materia, n.nota
        FROM notas n
        JOIN materias m ON n.idmateria = m.idmateria
        WHERE n.idaluno=%s
    """, (idaluno,))
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data
