from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Exame, Paciente
from app.schemas.schemas_exame import ExameCreate, ExameUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_exames(db: Session):
    logger.info("Buscando todos os exames.")
    exames = db.query(Exame).all()
    if not exames:
        logger.warning("Nenhum exame encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum exame encontrado"
        )
    logger.info(f"Encontrado {len(exames)} exames.")
    return exames


def get_exame_by_id(db: Session, exame_id: int):
    logger.info(f"Buscando exame com ID {exame_id}.")
    exame = db.query(Exame).filter(Exame.id_exame == exame_id).first()
    if not exame:
        logger.warning(f"Exame com o ID {exame_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exame com o ID {exame_id} não encontrado.",
        )
    logger.info(f"Exame com o ID {exame_id} encontrado.")
    return exame


def create_exame(db: Session, exame_data: ExameCreate):
    logger.info(f"Criando ID do exame para paciente {exame_data.id_paciente}.")
    paciente = (
        db.query(Paciente)
        .filter(Paciente.id_paciente == exame_data.id_paciente)
        .first()
    )
    if not paciente:
        logger.error(f"Paciente com o ID {exame_data.id_paciente} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paciente não encontrado com o id: {exame_data.id_paciente}",
        )

    new_exame = Exame(
        id_paciente=exame_data.id_paciente,
        tipo_exame=exame_data.tipo_exame,
        status=exame_data.status,
    )

    db.add(new_exame)
    db.commit()
    db.refresh(new_exame)
    logger.info(f"Exame criado com sucesso com ID {new_exame.id_exame}.")
    return new_exame


def update_exame(db: Session, exame_id: int, exame_data: ExameUpdate):
    logger.info(f"Atualizando exame com o ID {exame_id}.")
    exame = get_exame_by_id(db, exame_id)

    if exame_data.tipo_exame:
        logger.info(f"Atualizando tipo_exame para {exame_data.tipo_exame}.")
        exame.tipo_exame = exame_data.tipo_exame
    if exame_data.status:
        logger.info(f"Atualizando status para {exame_data.status}.")
        exame.status = exame_data.status

    db.commit()
    db.refresh(exame)
    logger.info(f"Exame com o ID {exame_id} atualizado com sucesso.")
    return exame


def delete_exame(db: Session, exame_id: int):
    logger.info(f"Deletando exame com o ID {exame_id}.")
    exame = get_exame_by_id(db, exame_id)

    db.delete(exame)
    db.commit()
    logger.info(f"Exame com ID {exame_id} deletado com sucesso do banco de dados.")
    return exame
