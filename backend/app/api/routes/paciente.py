from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_paciente import (
    get_all_pacientes,
    get_paciente_by_id,
    create_paciente,
    update_paciente,
    delete_paciente,
)
from app.schemas.schemas_paciente import (
    PacienteCreate,
    PacienteUpdate,
    PacienteOut,
    MensagemResposta,
)
from app.database.models.models_database import Usuario
from app.api.depends import get_db, get_current_usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

paciente_router = APIRouter(prefix="/paciente")


@paciente_router.get("/list", response_model=List[PacienteOut])
def list_pacientes_route(
    db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_usuario)
):
    logger.info(f"O usuário {current_user.nome} está listando todos os pacientes.")
    try:
        return get_all_pacientes(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar Pacientes - {str(e)}"
        )


@paciente_router.get("/view/{id_paciente}", response_model=PacienteOut)
def view_paciente_route(
    id_paciente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando o paciente com o ID {id_paciente}."
    )
    try:
        return get_paciente_by_id(db, id_paciente)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar o Paciente - {str(e)}"
        )


@paciente_router.post("/create", response_model=PacienteOut)
def add_paciente_route(
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(f"O usuário {current_user.nome} está criando um paciente.")
    try:
        return create_paciente(db, paciente)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao criar o Paciente - {str(e)}"
        )


@paciente_router.put("/update/{id_paciente}", response_model=PacienteOut)
def update_paciente_route(
    id_paciente: int,
    paciente: PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está atualizando o paciente com ID {id_paciente}."
    )

    try:
        return update_paciente(db, id_paciente, paciente)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar o Paciente - {str(e)}"
        )


@paciente_router.delete("/delete/{id_paciente}", response_model=MensagemResposta)
def delete_paciente_route(
    id_paciente: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_usuario),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo o paciente com ID {id_paciente}."
    )
    try:
        delete_paciente(db, id_paciente)
        return {"message": f"Paciente com ID {id_paciente} deletado com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao excluir paciente: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar o Paciente - {str(e)}"
        )
