from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import logging

from app.services.services_laudo import get_all_laudos, get_laudo_by_id, create_laudo, update_laudo, delete_laudo
from app.schemas.schemas_laudo import LaudoCreate, LaudoUpdate, LaudoOut
from app.api.depends import get_db, get_current_usuario

logger = logging.getLogger(__name__)

laudo_router = APIRouter(prefix="/laudo")

@laudo_router.get("/list", response_model=List[LaudoOut])
def list_laudos_route(db: Session = Depends(get_db), current_user = Depends(get_current_usuario)):
    try:
        return get_all_laudos(db)
    except Exception as e:
        logger.error(f"Erro ao listar todos os Laudos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar Laudos")

@laudo_router.get("/view/{id_laudo}", response_model=LaudoOut)
def view_laudo_route(id_laudo: int, db: Session = Depends(get_db), current_user = Depends(get_current_usuario)):
    try:
        return get_laudo_by_id(db, id_laudo)
    except Exception as e:
        logger.error(f"Erro ao listar o Laudo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar o Laudo")

@laudo_router.post("/create", response_model=LaudoOut)
def add_laudo_route(laudo: LaudoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_usuario)):
    try:
        return create_laudo(db, laudo)
    except Exception as e:
        logger.error(f"Erro ao criar o Laudo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar o Laudo")

@laudo_router.put("/update/{id_laudo}", response_model=LaudoOut)
def update_laudo_route(id_laudo: int, laudo: LaudoUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_usuario)):
    try:
        return update_laudo(db, id_laudo, laudo)
    except Exception as e:
        logger.error(f"Erro ao atualizar o Laudo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar o Laudo")

@laudo_router.delete("/delete/{id_laudo}", response_model=LaudoOut)
def delete_laudo_route(id_laudo: int, db: Session = Depends(get_db), current_user = Depends(get_current_usuario)):
    try:
        return delete_laudo(db, id_laudo)
    except Exception as e:
        logger.error(f"Erro ao deletar o Laudo: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao deletar o Laudo")
