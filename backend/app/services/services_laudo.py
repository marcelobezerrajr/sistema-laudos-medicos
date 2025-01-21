from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Laudo, Exame, Medico
from app.schemas.schemas_laudo import LaudoCreate, LaudoUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_laudos(db: Session):
    logger.info("Buscando todos os laudos.")
    laudos = db.query(Laudo).all()
    if not laudos:
        logger.warning("Nenhum laudo encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum laudo encontrado"
        )
    return laudos


def get_laudo_by_id(db: Session, laudo_id: int):
    logger.info(f"Buscando laudo com ID {laudo_id}.")
    laudo = db.query(Laudo).filter(Laudo.id_laudo == laudo_id).first()
    if not laudo:
        logger.warning(f"Laudo com o ID {laudo_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laudo com o ID {laudo_id} não encontrado.",
        )
    return laudo


def create_laudo(db: Session, laudo_data: LaudoCreate):
    logger.info(f"Criando ID do laudo para médico {laudo_data.id_medico}.")
    exame = db.query(Exame).filter(Exame.id_exame == laudo_data.id_exame).first()
    if not exame:
        logger.error(f"Exame com o ID {laudo_data.id_exame} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exame com o ID {laudo_data.id_exame} não encontrado.",
        )

    medico = db.query(Medico).filter(Medico.id_medico == laudo_data.id_medico).first()
    if not medico:
        logger.error(f"Médico com o ID {laudo_data.id_medico} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico com o ID {laudo_data.id_medico} não encontrado.",
        )

    new_laudo = Laudo(
        id_exame=laudo_data.id_exame,
        id_medico=laudo_data.id_medico,
        conteudo=laudo_data.conteudo,
    )
    db.add(new_laudo)
    db.commit()
    db.refresh(new_laudo)
    logger.info(f"Laudo criado com sucesso com o ID {new_laudo.id_laudo}")
    return new_laudo


def update_laudo(db: Session, laudo_id: int, laudo_data: LaudoUpdate):
    logger.info(f"Atualizando laudo com o ID {laudo_id}.")
    laudo = db.query(Laudo).filter(Laudo.id_laudo == laudo_id).first()
    if not laudo:
        logger.error(f"Laudo com o ID {laudo_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laudo com o ID {laudo_id} não encontrado.",
        )

    if laudo_data.conteudo:
        logger.info(f"Atualizando conteudo para {laudo_data.conteudo}.")
        laudo.conteudo = laudo_data.conteudo

    db.commit()
    db.refresh(laudo)
    logger.info(f"Laudo com o ID {laudo_id} atualizado com sucesso.")
    return laudo


def delete_laudo(db: Session, laudo_id: int):
    logger.info(f"Deletando laudo com o ID {laudo_id}.")
    laudo = get_laudo_by_id(db, laudo_id)

    db.delete(laudo)
    db.commit()
    logger.info(f"Laudo com ID {laudo_id} deletado com sucesso do banco de dados.")
    return laudo
