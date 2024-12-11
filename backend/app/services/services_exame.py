from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Exame, Paciente
from app.schemas.schemas_exame import ExameCreate, ExameUpdate

logger = logging.getLogger(__name__)

def get_all_exames(db: Session):
    exames = db.query(Exame).all()
    if not exames:
        logger.warning("Nenhum exame encontrado.")
    return exames

def get_exame_by_id(db: Session, exame_id: int):
    exame = db.query(Exame).filter(Exame.id_exame == exame_id).first()
    if not exame:
        logger.error(f"Exame não encontrado com id: {exame_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exame não encontrado")
    return exame

def create_exame(db: Session, exame_data: ExameCreate):
    paciente = db.query(Paciente).filter(Paciente.id_paciente == exame_data.id_paciente).first()
    if not paciente:
        logger.error(f"Paciente não encontrado com id: {exame_data.id_paciente}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    new_exame = Exame(
        id_paciente=exame_data.id_paciente,
        tipo_exame=exame_data.tipo_exame,
        status=exame_data.status
    )
    
    db.add(new_exame)
    db.commit()
    db.refresh(new_exame)
    logger.info(f"Exame criado com sucesso: {new_exame.id_exame}")
    return new_exame

def update_exame(db: Session, exame_id: int, exame_data: ExameUpdate):
    exame = get_exame_by_id(db, exame_id)
    
    exame.tipo_exame = exame_data.tipo_exame or exame.tipo_exame
    exame.status = exame_data.status or exame.status

    db.commit()
    db.refresh(exame)
    logger.info(f"Exame atualizado com sucesso: {exame_id}")
    return exame

def delete_exame(db: Session, exame_id: int):
    exame = get_exame_by_id(db, exame_id)

    db.delete(exame)
    db.commit()
    logger.info(f"Exame deletado com sucesso: {exame_id}")
    return exame
