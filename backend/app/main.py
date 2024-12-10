from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.database.database import Base, engine
from app.api.routes import usuario, medico, paciente, exame, laudo

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

def configure_all(app: FastAPI):
    configure_routes(app)
    configure_db()

def configure_routes(app: FastAPI):
    app.include_router(usuario.usuario_router, tags=["Usuário"])
    app.include_router(medico.medico_router, tags=["Médico"])
    app.include_router(paciente.paciente_router, tags=["Paciente"])
    app.include_router(exame.exame_router, tags=["Exame"])
    app.include_router(laudo.laudo_router, tags=["Laudo"])

def configure_db():
    Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "details": str(exc), "request": request.url},
    )

configure_all(app)

@app.get("/")
def root():
    return {"message": "Go to /docs!"}
