from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_paciente import get_all_pacientes, get_paciente_by_id, create_paciente, update_paciente, delete_paciente
from app.schemas.schemas_paciente import PacienteCreate, PacienteUpdate, PacienteOut
from app.api.depends import get_db, get_current_usuario

logger = logging.getLogger(__name__)

paciente_router = APIRouter(prefix="/paciente")


@paciente_router.get("/list", response_model=List[PacienteOut])
def list_pacientes_route(db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    try:
        return get_all_pacientes(db)
    except Exception as e:
        logger.error(f"Erro ao listar todos os Pacientes: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar Pacientes")


@paciente_router.get("/view/{id_paciente}", response_model=PacienteOut)
def view_paciente_route(id_paciente: int, db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    try:
        return get_paciente_by_id(db, id_paciente)
    except Exception as e:
        logger.error(f"Erro ao listar o Paciente: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao listar o Paciente")


@paciente_router.post("/create", response_model=PacienteOut)
def add_paciente_route(paciente: PacienteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    try:
        return create_paciente(db, paciente)
    except Exception as e:
        logger.error(f"Erro ao criar o Paciente: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar o Paciente")


@paciente_router.put("/update/{id_paciente}", response_model=PacienteOut)
def update_paciente_route(id_paciente: int, paciente: PacienteUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    try:
        return update_paciente(db, id_paciente, paciente)
    except Exception as e:
        logger.error(f"Erro ao atualizar o Paciente: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao atualizar o Paciente")


@paciente_router.delete("/delete/{id_paciente}", response_model=PacienteOut)
def delete_paciente_route(id_paciente: int, db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    try:
        return delete_paciente(db, id_paciente)
    except Exception as e:
        logger.error(f"Erro ao deletar o Paciente: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao deletar o Paciente")
