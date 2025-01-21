from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_laudo import (
    get_all_laudos,
    get_laudo_by_id,
    create_laudo,
    update_laudo,
    delete_laudo,
)
from app.database.models.models_database import Usuario
from app.schemas.schemas_laudo import LaudoCreate, LaudoUpdate, LaudoOut
from app.api.depends import get_db, get_current_usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

laudo_router = APIRouter(prefix="/laudo")


@laudo_router.get("/list", response_model=List[LaudoOut])
def list_laudos_route(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_usuario)
):
    logger.info(f"O usuário {current_user.nome} está listando todos os laudos.")
    try:
        return get_all_laudos(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar Laudos - {str(e)}")


@laudo_router.get("/view/{id_laudo}", response_model=LaudoOut)
def view_laudo_route(
    id_laudo: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando o laudo com o ID {id_laudo}."
    )
    try:
        return get_laudo_by_id(db, id_laudo)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar o Laudo - {str(e)}"
        )


@laudo_router.post("/create", response_model=LaudoOut)
def add_laudo_route(
    laudo: LaudoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(f"O usuário {current_user.nome} está criando um laudo.")
    try:
        return create_laudo(db, laudo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar o Laudo - {str(e)}")


@laudo_router.put("/update/{id_laudo}", response_model=LaudoOut)
def update_laudo_route(
    id_laudo: int,
    laudo: LaudoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está atualizando o laudo com ID {id_laudo}."
    )
    try:
        return update_laudo(db, id_laudo, laudo)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar o Laudo - {str(e)}"
        )


@laudo_router.delete("/delete/{id_laudo}", response_model=LaudoOut)
def delete_laudo_route(
    id_laudo: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo o laudo com ID {id_laudo}."
    )
    try:
        return delete_laudo(db, id_laudo)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar o Laudo - {str(e)}"
        )
