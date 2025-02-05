from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_usuario import (
    get_all_usuarios,
    get_usuario_by_id,
    create_usuario,
    update_usuario,
    delete_usuario,
)
from app.schemas.schemas_usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioListResponse,
    MensagemResposta,
)
from app.database.models.models_database import Usuario
from app.api.depends import get_db, get_current_usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

usuario_router = APIRouter(prefix="/usuario")


@usuario_router.get("/list", response_model=List[UsuarioListResponse])
def list_usuarios_route(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_usuario)
):
    logger.info(f"O usuário {current_user.nome} está listando todos os usuários.")
    try:
        return get_all_usuarios(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar Usuários - {str(e)}"
        )


@usuario_router.get("/view/{id_usuario}", response_model=UsuarioListResponse)
def view_usuario_route(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando o usuário com o ID {id_usuario}."
    )
    try:
        return get_usuario_by_id(db, id_usuario)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar o Usuário - {str(e)}"
        )


@usuario_router.post("/create", response_model=UsuarioBase)
def add_usuario_route(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return create_usuario(db, usuario)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao criar o Usuário - {str(e)}"
        )


@usuario_router.put("/update/{id_usuario}", response_model=UsuarioBase)
def update_usuario_route(
    id_usuario: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está atualizando o usuário com ID {id_usuario}."
    )
    try:
        return update_usuario(db, id_usuario, usuario)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar o Usuário - {str(e)}"
        )


@usuario_router.delete("/delete/{id_usuario}", response_model=MensagemResposta)
def delete_usuario_route(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo o usuário com ID {id_usuario}."
    )
    try:
        delete_usuario(db, id_usuario)
        return {"message": f"Usuário com ID {id_usuario} deletado com sucesso."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar o Usuário - {str(e)}"
        )
