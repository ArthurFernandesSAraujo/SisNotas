from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import conectar_bd, fechar_bd

router = APIRouter(prefix="/secretaria", tags=["Secretaria / Admin"])

# =============================================
#       MODELOS JSON (Pydantic)
# =============================================

class ProfessorCreate(BaseModel):
    nome: str
    email: str
    usuario: str
    senha: str

class AlunoIn(BaseModel):
    nome: str
    matricula: str
    email: str


# =============================================
#  PROFESSORES
# =============================================

@router.get("/professores")
def listar_professores():
    con, cur = conectar_bd()
    cur.execute("""
        SELECT idprofessor, nome, email 
        FROM professores
    """)
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data


@router.post("/professores")
def cadastrar_professor(data: ProfessorCreate):
    con, cur = conectar_bd()

    # Cria usuário para login
    cur.execute("""
        INSERT INTO usuarios (nome, username, senha, nivel)
        VALUES (%s, %s, %s, 'professor')
    """, (data.nome, data.usuario, data.senha))

    # Cadastra professor (SEM telefone e SEM idusuario)
    cur.execute("""
        INSERT INTO professores (nome, email)
        VALUES (%s, %s)
    """, (data.nome, data.email))

    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor cadastrado com sucesso!"}


@router.put("/professores/{idprofessor}")
def atualizar_professor(idprofessor: int, data: ProfessorCreate):
    con, cur = conectar_bd()

    cur.execute("""
        UPDATE professores
        SET nome=%s, email=%s
        WHERE idprofessor=%s
    """, (data.nome, data.email, idprofessor))

    # Atualiza usuário correspondente pelo nome
    cur.execute("""
        UPDATE usuarios
        SET username=%s, senha=%s
        WHERE nome=%s AND nivel='professor'
    """, (data.usuario, data.senha, data.nome))

    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor atualizado com sucesso!"}


@router.delete("/professores/{idprofessor}")
def excluir_professor(idprofessor: int):
    con, cur = conectar_bd()

    # pega nome para excluir usuário correspondente
    cur.execute("SELECT nome FROM professores WHERE idprofessor=%s", (idprofessor,))
    row = cur.fetchone()

    if not row:
        fechar_bd(con, cur)
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    nome_prof = row["nome"]

    cur.execute("DELETE FROM professores WHERE idprofessor=%s", (idprofessor,))
    cur.execute("DELETE FROM usuarios WHERE nome=%s AND nivel='professor'", (nome_prof,))

    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Professor excluído com sucesso!"}



# =============================================
#  ALUNOS
# =============================================

@router.get("/alunos")
def listar_alunos():
    con, cur = conectar_bd()
    cur.execute("SELECT * FROM alunos")
    data = cur.fetchall()
    fechar_bd(con, cur)
    return data


@router.post("/alunos")
def cadastrar_aluno(data: AlunoIn):
    con, cur = conectar_bd()
    cur.execute("""
        INSERT INTO alunos (nome, matricula, email)
        VALUES (%s, %s, %s)
    """, (data.nome, data.matricula, data.email))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno cadastrado com sucesso"}


@router.put("/alunos/{idaluno}")
def atualizar_aluno(idaluno: int, data: AlunoIn):
    con, cur = conectar_bd()
    cur.execute("""
        UPDATE alunos
        SET nome=%s, matricula=%s, email=%s
        WHERE idaluno=%s
    """, (data.nome, data.matricula, data.email, idaluno))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno atualizado com sucesso"}


@router.delete("/alunos/{idaluno}")
def excluir_aluno(idaluno: int):
    con, cur = conectar_bd()
    cur.execute("DELETE FROM alunos WHERE idaluno=%s", (idaluno,))
    con.commit()
    fechar_bd(con, cur)
    return {"msg": "Aluno excluído com sucesso"}
