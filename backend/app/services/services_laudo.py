from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Laudo, Exame, Medico
from app.schemas.schemas_laudo import LaudoCreate, LaudoUpdate

logger = logging.getLogger(__name__)

def get_all_laudos(db: Session):
    laudos = db.query(Laudo).all()
    if not laudos:
        logger.warning("Nenhum laudo encontrado.")
    return laudos

def get_laudo_by_id(db: Session, laudo_id: int):
    laudo = db.query(Laudo).filter(Laudo.id_laudo == laudo_id).first()
    if not laudo:
        logger.error(f"Laudo não encontrado com id: {laudo_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laudo não encontrado")
    return laudo

def create_laudo(db: Session, laudo_data: LaudoCreate):
    exame = db.query(Exame).filter(Exame.id_exame == laudo_data.id_exame).first()
    if not exame:
        logger.error(f"Exame não encontrado com id: {laudo_data.id_exame}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exame não encontrado")
    
    medico = db.query(Medico).filter(Medico.id_medico == laudo_data.id_medico).first()
    if not medico:
        logger.error(f"Médico não encontrado com id: {laudo_data.id_medico}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    new_laudo = Laudo(
        id_exame=laudo_data.id_exame,
        id_medico=laudo_data.id_medico,
        conteudo=laudo_data.conteudo
    )
    db.add(new_laudo)
    db.commit()
    db.refresh(new_laudo)
    logger.info(f"Laudo criado com sucesso: {new_laudo.id_laudo}")
    return new_laudo

def update_laudo(db: Session, laudo_id: int, laudo_data: LaudoUpdate):
    laudo = db.query(Laudo).filter(Laudo.id_laudo == laudo_id).first()
    if not laudo:
        logger.error(f"Laudo não encontrado com id: {laudo_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laudo não encontrado")
    
    if laudo_data.conteudo:
        laudo.conteudo = laudo_data.conteudo

    db.commit()
    db.refresh(laudo)
    logger.info(f"Laudo atualizado com sucesso: {laudo_id}")
    return laudo

def delete_laudo(db: Session, laudo_id: int):
    laudo = db.query(Laudo).filter(Laudo.id_laudo == laudo_id).first()
    if not laudo:
        logger.error(f"Laudo não encontrado com id: {laudo_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laudo não encontrado")

    db.delete(laudo)
    db.commit()
    logger.info(f"Laudo deletado com sucesso: {laudo_id}")
    return laudo
