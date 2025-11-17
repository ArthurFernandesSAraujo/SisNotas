from fastapi import APIRouter, HTTPException
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(username: str, senha: str, tipo: str):
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM usuarios WHERE username=%s AND senha=%s", (username, senha))
    user = cur.fetchone()
    fechar_bd(con, cur)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    if user["nivel"] != tipo:
        raise HTTPException(status_code=403, detail="Tipo de usuário incorreto")

    return user  
