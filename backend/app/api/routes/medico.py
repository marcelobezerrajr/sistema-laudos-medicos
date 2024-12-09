from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_medico import get_all_medicos, get_medico_by_id, create_medico, update_medico, delete_medico
from app.schemas.schemas_medico import MedicoCreate, MedicoUpdate, MedicoOut
from app.api.depends import get_db

logger = logging.getLogger(__name__)

medico_router = APIRouter(prefix="/medicos")

@medico_router.get("/list", response_model=List[MedicoOut])
def list_medicos_route(db: Session = Depends(get_db)):
    try:
        return get_all_medicos(db)
    except Exception as e:
        logger.error(f"Erro ao listar todos os Médicos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar Médicos")

@medico_router.get("/view/{id_medico}", response_model=MedicoOut)
def view_medico_route(id_medico: int, db: Session = Depends(get_db)):
    try:
        return get_medico_by_id(db, id_medico)
    except Exception as e:
        logger.error(f"Erro ao listar o Médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar o Médico")

@medico_router.post("/create", response_model=MedicoOut)
def add_medico_route(medico: MedicoCreate, db: Session = Depends(get_db)):
    try:
        return create_medico(db, medico)
    except Exception as e:
        logger.error(f"Erro ao criar o Médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar o Médico")

@medico_router.put("/update/{id_medico}", response_model=MedicoOut)
def update_medico_route(id_medico: int, medico: MedicoUpdate, db: Session = Depends(get_db)):
    try:
        return update_medico(db, id_medico, medico)
    except Exception as e:
        logger.error(f"Erro ao atualizar o Médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar o Médico")

@medico_router.delete("/delete/{id_medico}", response_model=MedicoOut)
def delete_medico_route(id_medico: int, db: Session = Depends(get_db)):
    try:
        return delete_medico(db, id_medico)
    except Exception as e:
        logger.error(f"Erro ao deletar o Médico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao deletar o Médico")
