from fastapi import FastAPI
from routers import (
    auth,
    alunos,
    professores,
    materias,
    notas,
    associacoes,
    secretaria
)

app = FastAPI(
    title="Sistema de Notas - API",
    description="API oficial do sistema de gerenciamento de notas (Secretaria, Professores e Alunos)",
    version="1.0.0"
)

# ============================
#  🔗 REGISTRO DOS ROUTERS
# ============================

app.include_router(auth.router)
app.include_router(alunos.router)
app.include_router(professores.router)
app.include_router(materias.router)
app.include_router(notas.router)
app.include_router(associacoes.router)
app.include_router(secretaria.router)


# ============================
#  🌐 ROTA PADRÃO
# ============================
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "API do Sistema de Notas funcionando!",
        "docs": "Acesse /docs para visualizar a documentação automática"
    }
