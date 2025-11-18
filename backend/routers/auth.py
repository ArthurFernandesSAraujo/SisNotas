from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginIn(BaseModel):
    username: str
    senha: str
    tipo: str

@router.post("/login")
def login(data: LoginIn):
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM usuarios WHERE username=%s AND senha=%s",
                (data.username, data.senha))

    user = cur.fetchone()
    fechar_bd(con, cur)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    if user["nivel"] != data.tipo:
        raise HTTPException(status_code=403, detail="Tipo de usuário incorreto")

    return {
        "id": user["idusuarios"],
        "nome": user["nome"],
        "username": user["username"],
        "nivel": user["nivel"]
    }
