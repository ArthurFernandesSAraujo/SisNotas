from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/professores", tags=["Professores"])

@router.get("/")
def listar_professores():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM professores")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/")
def cadastrar_professor(nome: str, email: str):
    con, cur = conectar_bd()
    cur.execute("INSERT INTO professores (nome, email) VALUES (%s, %s)", (nome, email))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor cadastrado!"}

@router.get("/{idprof}/materias")
def materias_do_professor(idprof: int):
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM materias WHERE idprofessor=%s", (idprof,))
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data
