from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from app.database.database import Base, engine
from app.api.routes import usuario

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

def configure_all(app: FastAPI):
    configure_routes(app)
    configure_db()

def configure_routes(app: FastAPI):
    app.include_router(usuario.usuario_router, tags=["Usuários"])

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
