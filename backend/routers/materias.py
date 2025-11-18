from fastapi import APIRouter
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/materias", tags=["Matérias"])

# ============================================
# LISTAR MATÉRIAS
# ============================================
@router.get("/")
def listar_materias():
    con, cur = conectar_bd()

    cur.execute("""
        SELECT 
            m.idmateria,
            m.nome,
            p.idprofessor,
            p.nome AS professor_nome
        FROM materias m
        LEFT JOIN professores p ON m.idprofessor = p.idprofessor
    """)

    dados = cur.fetchall()  # <-- agora é uma lista de dicionários

    fechar_bd(con, cur)

    return dados

# ============================================
# CADASTRAR MATÉRIA
# ============================================
@router.post("/")
def cadastrar_materia(nome: str):
    con, cur = conectar_bd()
    cur.execute("INSERT INTO materias (nome) VALUES (%s)", (nome,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria cadastrada!"}

# ============================================
# EXCLUIR MATÉRIA
# ============================================
@router.delete("/{idmateria}")
def excluir_materia(idmateria: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM materias WHERE idmateria = %s", (idmateria,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Matéria excluída com sucesso!"}
