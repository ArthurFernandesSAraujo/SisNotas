from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    description="API oficial do sistema de gerenciamento de notas",
    version="1.0.0"
)

# ============================
#  CORS CORRIGIDO 🔥🔥🔥
# ============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # DOMÍNIO DO ANGULAR
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
#  ROTAS
# ============================

app.include_router(auth.router)
app.include_router(alunos.router)
app.include_router(professores.router)
app.include_router(materias.router)
app.include_router(notas.router)
app.include_router(associacoes.router)
app.include_router(secretaria.router)

@app.get("/")
def root():
    return {"status": "online"}
