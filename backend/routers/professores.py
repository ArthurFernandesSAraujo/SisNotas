from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/professores", tags=["Professores"])


# =============================
# LISTAR TODOS OS PROFESSORES
# =============================
@router.get("/")
def listar_professores():
    con, cur = conectar_bd()
    cur.execute("SELECT idprofessor, nome, email FROM professores")
    rows = cur.fetchall()
    fechar_bd(con, cur)
    return rows


# =============================
# LISTAR MATÉRIAS DO PROFESSOR
# =============================
@router.get("/{idprof}/materias")
def materias_do_professor(idprof: int):
    con, cur = conectar_bd()

    cur.execute("""
        SELECT 
            m.idmateria,
            m.nome AS nome,
            p.nome AS professor
        FROM materias m
        LEFT JOIN professores p ON p.idprofessor = m.idprofessor
        WHERE m.idprofessor = %s
    """, (idprof,))

    rows = cur.fetchall()
    fechar_bd(con, cur)
    return rows


# =============================
# LISTAR ALUNOS DE UMA MATÉRIA
# =============================
@router.get("/{idprof}/materias/{idmateria}/alunos")
def alunos_da_materia(idprof: int, idmateria: int):
    con, cur = conectar_bd()

    # garantir que matéria realmente pertence ao professor
    cur.execute("""
        SELECT idmateria FROM materias 
        WHERE idmateria=%s AND idprofessor=%s
    """, (idmateria, idprof))
    materia_valida = cur.fetchone()

    if not materia_valida:
        fechar_bd(con, cur)
        return {"erro": "Esta matéria não pertence a este professor."}

    cur.execute("""
        SELECT 
            a.idaluno,
            a.nome,
            COALESCE(n.nota, NULL) AS nota
        FROM aluno_materias am
        INNER JOIN alunos a ON a.idaluno = am.idaluno
        LEFT JOIN notas n ON n.idaluno = a.idaluno 
                          AND n.idmateria = am.idmateria
        WHERE am.idmateria = %s
    """, (idmateria,))

    rows = cur.fetchall()
    fechar_bd(con, cur)
    return rows


# =============================
# SALVAR NOTA DO ALUNO
# =============================
@router.post("/notas/{idaluno}")
def salvar_nota(idaluno: int, idmateria: int, nota: float):
    con, cur = conectar_bd()

    # existe nota?
    cur.execute("""
        SELECT idnota FROM notas WHERE idaluno=%s AND idmateria=%s
    """, (idaluno, idmateria))
    existe = cur.fetchone()

    if existe:
        cur.execute("""
            UPDATE notas
            SET nota=%s
            WHERE idaluno=%s AND idmateria=%s
        """, (nota, idaluno, idmateria))
    else:
        cur.execute("""
            INSERT INTO notas (idaluno, idmateria, nota)
            VALUES (%s, %s, %s)
        """, (idaluno, idmateria, nota))

    con.commit()
    fechar_bd(con, cur)

    return {"msg": "Nota salva com sucesso!", "idaluno": idaluno, "idmateria": idmateria, "nota": nota}
