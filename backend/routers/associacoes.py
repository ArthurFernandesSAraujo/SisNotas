from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/associacoes", tags=["Associações"])


# ============================
# ASSOCIAR PROFESSOR → MATÉRIA
# ============================
@router.post("/professor-materia")
def associar_professor(idprofessor: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute("UPDATE materias SET idprofessor=%s WHERE idmateria=%s",
                (idprofessor, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor associado à matéria!"}


# ============================
# ASSOCIAR ALUNO → MATÉRIA
# ============================
@router.post("/aluno-materia")
def associar_aluno(idaluno: int, idmateria: int):
    con, cur = conectar_bd()
    cur.execute("""
        INSERT IGNORE INTO aluno_materias (idaluno, idmateria)
        VALUES (%s, %s)
    """, (idaluno, idmateria))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno matriculado na matéria!"}


# ============================
# LISTAR ALUNOS DA MATÉRIA
# ============================
@router.get("/materia/{idmateria}/alunos")
def alunos_materia(idmateria: int):
    con, cur = conectar_bd()
    cur.execute("""
        SELECT a.idaluno, a.nome, a.email
        FROM aluno_materias am
        JOIN alunos a ON a.idaluno = am.idaluno
        WHERE am.idmateria=%s
    """, (idmateria,))
    data = cur.fetchall()
    fechar_bd(con, cur)

    alunos = []
    for a in data:
        alunos.append({
            "idaluno": a[0],
            "nome": a[1],
            "email": a[2]
        })

    return alunos
