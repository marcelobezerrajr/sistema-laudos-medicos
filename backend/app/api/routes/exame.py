from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_exame import (
    get_all_exames,
    get_exame_by_id,
    create_exame,
    update_exame,
    delete_exame,
)
from app.schemas.schemas_exame import ExameCreate, ExameUpdate, ExameOut
from app.database.models.models_database import Usuario
from app.api.depends import get_db, get_current_usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

exame_router = APIRouter(prefix="/exame")


@exame_router.get("/list", response_model=List[ExameOut])
def list_exames_route(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_usuario)
):
    logger.info(f"O usuário {current_user.nome} está listando todos os exames.")
    try:
        return get_all_exames(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar Exames - {str(e)}")


@exame_router.get("/view/{id_exame}", response_model=ExameOut)
def view_exame_route(
    id_exame: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando o exame com o ID {id_exame}."
    )
    try:
        return get_exame_by_id(db, id_exame)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao visualizar o Exame - {str(e)}"
        )


@exame_router.post("/create", response_model=ExameOut)
def add_exame_route(
    exame: ExameCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(f"O usuário {current_user.nome} está criando um exame.")
    try:
        return create_exame(db, exame)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar o Exame - {str(e)}")


@exame_router.put("/update/{id_exame}", response_model=ExameOut)
def update_exame_route(
    id_exame: int,
    exame: ExameUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está atualizando o exame com ID {id_exame}."
    )
    try:
        return update_exame(db, id_exame, exame)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar o Exame - {str(e)}"
        )


@exame_router.delete("/delete/{id_exame}", response_model=ExameOut)
def delete_exame_route(
    id_exame: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo o exame com ID {id_exame}."
    )
    try:
        return delete_exame(db, id_exame)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar o Exame - {str(e)}"
        )
