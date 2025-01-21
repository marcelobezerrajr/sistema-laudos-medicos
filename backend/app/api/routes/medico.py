from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_medico import (
    get_all_medicos,
    get_medico_by_id,
    create_medico,
    update_medico,
    delete_medico,
)
from app.database.models.models_database import Usuario
from app.schemas.schemas_medico import MedicoCreate, MedicoUpdate, MedicoOut
from app.api.depends import get_db, get_current_usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

medico_router = APIRouter(prefix="/medico")


@medico_router.get("/list", response_model=List[MedicoOut])
def list_medicos_route(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(f"O usuário {current_user.nome} está listando todos os médicos.")
    try:
        return get_all_medicos(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar Médicos - {str(e)}"
        )


@medico_router.get("/view/{id_medico}", response_model=MedicoOut)
def view_medico_route(
    id_medico: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando o médico com o ID {id_medico}."
    )
    try:
        return get_medico_by_id(db, id_medico)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar o Médico - {str(e)}"
        )


@medico_router.post("/create", response_model=MedicoOut)
def add_medico_route(
    medico: MedicoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(f"O usuário {current_user.nome} está adicionando um médico.")
    try:
        return create_medico(db, medico)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao criar o Médico - {str(e)}"
        )


@medico_router.put("/update/{id_medico}", response_model=MedicoOut)
def update_medico_route(
    id_medico: int,
    medico: MedicoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está atualizando o médico com ID {id_medico}."
    )
    try:
        return update_medico(db, id_medico, medico)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar o Médico - {str(e)}"
        )


@medico_router.delete("/delete/{id_medico}", response_model=MedicoOut)
def delete_medico_route(
    id_medico: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo o médico com ID {id_medico}."
    )
    try:
        return delete_medico(db, id_medico)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar o Médico - {str(e)}"
        )
