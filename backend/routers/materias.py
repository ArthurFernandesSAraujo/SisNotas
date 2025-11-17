from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/materias", tags=["Matérias"])

@router.get("/")
def listar():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM materias")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data

@router.post("/")
def cadastrar(nome: str):
    con, cur = conectar_bd()
    cur.execute("INSERT INTO materias (nome) VALUES (%s)", (nome,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria cadastrada!"}
