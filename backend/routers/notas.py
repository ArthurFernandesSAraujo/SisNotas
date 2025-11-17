from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/notas", tags=["Notas"])

@router.post("/")
def lancar(idaluno: int, idmateria: int, idprofessor: int, nota: float):
    con, cur = conectar_bd()
    cur.execute("""
        INSERT INTO notas (idaluno, idmateria, idprofessor, nota)
        VALUES (%s, %s, %s, %s)
    """, (idaluno, idmateria, idprofessor, nota))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota lançada!"}

@router.put("/{idnota}")
def atualizar(idnota: int, nota: float):
    con, cur = conectar_bd()
    cur.execute("UPDATE notas SET nota=%s WHERE idnota=%s", (nota, idnota))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota atualizada!"}

@router.delete("/{idnota}")
def excluir(idnota: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM notas WHERE idnota=%s", (idnota,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Nota excluída!"}
