from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_usuario import get_all_usuarios, get_usuario_by_id, create_usuario, update_usuario, delete_usuario
from app.schemas.schemas_usuario import UsuarioBase, UsuarioCreate, UsuarioUpdate, UsuarioListResponse
from app.api.depends import get_db

logger = logging.getLogger(__name__)

usuario_router = APIRouter(prefix="/usuario")

@usuario_router.get("/list", response_model=List[UsuarioListResponse])
def list_usuarios_route(db: Session = Depends(get_db)):
    try:
        return get_all_usuarios(db)
    except Exception as e:
        logger.error(f"Erro ao listar todos os Usuários: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar Usuários")

@usuario_router.get("/view/{id_usuario}", response_model=UsuarioListResponse)
def view_usuario_route(id_usuario: int, db: Session = Depends(get_db)):
    try:
        return get_usuario_by_id(db, id_usuario)
    except Exception as e:
        logger.error(f"Erro ao listar o Usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar o Usuário")

@usuario_router.post("/create", response_model=UsuarioBase)
def add_usuario_route(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return create_usuario(db, usuario)
    except Exception as e:
        logger.error(f"Erro ao criar o Usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar o Usuário")

@usuario_router.put("/update/{id_usuario}", response_model=UsuarioBase)
def update_usuario_route(id_usuario: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        return update_usuario(db, id_usuario, usuario)
    except Exception as e:
        logger.error(f"Erro ao atualizar o Usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar o Usuário")

@usuario_router.delete("/delete/{id_usuario}", response_model=UsuarioBase)
def delete_usuario_route(id_usuario: int, db: Session = Depends(get_db)):
    try:
        return delete_usuario(db, id_usuario)
    except Exception as e:
        logger.error(f"Erro ao deletar o Usuário: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao deletar o Usuário")
