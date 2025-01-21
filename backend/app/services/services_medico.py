from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Medico, Usuario
from app.schemas.schemas_medico import MedicoCreate, MedicoUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_medicos(db: Session):
    logger.info("Buscando todos os médicos.")
    medicos = db.query(Medico).all()
    if not medicos:
        logger.warning("Nenhum médico encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum médico encontrado"
        )
    return medicos


def get_medico_by_id(db: Session, medico_id: int):
    logger.info(f"Buscando médico com ID {medico_id}.")
    medico = db.query(Medico).filter(Medico.id_medico == medico_id).first()
    if not medico:
        logger.warning(f"Médico com o ID {medico_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico com o ID {medico_id} não encontrado.",
        )
    return medico


def create_medico(db: Session, medico_data: MedicoCreate):
    logger.info(f"Criando médico {medico_data.id_usuario}.")
    if db.query(Medico).filter(Medico.crm == medico_data.crm).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CRM já cadastrado"
        )

    usuario = (
        db.query(Usuario).filter(Usuario.id_usuario == medico_data.id_usuario).first()
    )
    if not usuario:
        logger.error(f"Usuário com o ID {medico_data.id_usuario} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com o ID {medico_data.id_usuario} não encontrado.",
        )

    if usuario.tipo != "medico":
        logger.error(
            f"Usuário com o id {medico_data.id_usuario} não é médico, operação não permitida"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário com o id {medico_data.id_usuario} não é médico, operação não permitida",
        )

    new_medico = Medico(
        id_medico=medico_data.id_usuario,
        especialidade=medico_data.especialidade,
        crm=medico_data.crm,
    )

    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    logger.info(f"Médico criado com sucesso com ID {medico_data.id_usuario}.")
    return new_medico


def update_medico(db: Session, medico_id: int, medico_data: MedicoUpdate):
    logger.info(f"Atualizando médico com o ID {medico_id}.")
    if (
        medico_data.crm
        and db.query(Medico).filter(Medico.crm == medico_data.crm).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CRM já cadastrado"
        )

    medico = get_medico_by_id(db, medico_id)

    medico.especialidade = medico_data.especialidade or medico.especialidade
    medico.crm = medico_data.crm or medico.crm

    db.commit()
    db.refresh(medico)
    logger.info(f"Médico com o ID {medico_id} atualizado com sucesso.")
    return medico


def delete_medico(db: Session, medico_id: int):
    logger.info(f"Deletando médico com o ID {medico_id}.")
    medico = get_medico_by_id(db, medico_id)

    db.delete(medico)
    db.commit()
    logger.info(f"Médico com ID {medico_id} deletado com sucesso do banco de dados.")
    return {"message": f"Médico com ID {medico_id} deletado com sucesso."}
