from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/associacoes", tags=["Associações"])

@router.post("/aluno-materia")
def aluno_materia(idaluno: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute("INSERT IGNORE INTO aluno_materias (idaluno, idmateria) VALUES (%s, %s)",
                (idaluno, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno matriculado na matéria!"}

@router.post("/professor-materia")
def professor_materia(idprofessor: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute("UPDATE materias SET idprofessor=%s WHERE idmateria=%s",
                (idprofessor, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor associado à matéria!"}
