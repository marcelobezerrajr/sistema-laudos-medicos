from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Medico, Usuario
from app.schemas.schemas_medico import MedicoCreate, MedicoUpdate

logger = logging.getLogger(__name__)


def get_all_medicos(db: Session):
    medicos = db.query(Medico).all()
    if not medicos:
        logger.warning("Nenhum médico encontrado.")
    return medicos


def get_medico_by_id(db: Session, medico_id: int):
    medico = db.query(Medico).filter(Medico.id_medico == medico_id).first()
    if not medico:
        logger.error(f"Médico não encontrado com id: {medico_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")
    return medico


def create_medico(db: Session, medico_data: MedicoCreate):
    if db.query(Medico).filter(Medico.crm == medico_data.crm).first():
        logger.warning(f"Tentativa de criar um médico com CRM existente: {
                       medico_data.crm}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CRM já cadastrado")

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == medico_data.id_usuario).first()
    if not usuario:
        logger.error(f"Usuário não encontrado com id: {
                     medico_data.id_usuario}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")

    if usuario.tipo != 'medico':
        logger.error(f"Usuário com o id: {
                     medico_data.id_usuario} não é médico, operação não permitida.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não é médico")

    new_medico = Medico(
        id_medico=medico_data.id_usuario,
        especialidade=medico_data.especialidade,
        crm=medico_data.crm
    )

    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    logger.info(f"Médico com CRM {new_medico.crm} criado com sucesso.")
    return new_medico


def update_medico(db: Session, medico_id: int, medico_data: MedicoUpdate):
    medico = get_medico_by_id(db, medico_id)

    medico.especialidade = medico_data.especialidade or medico.especialidade
    medico.crm = medico_data.crm or medico.crm

    db.commit()
    db.refresh(medico)
    logger.info(f"Médico com id {medico_id} atualizado com sucesso.")
    return medico


def delete_medico(db: Session, medico_id: int):
    medico = get_medico_by_id(db, medico_id)

    db.delete(medico)
    db.commit()
    logger.info(f"Médico com id {medico_id} deletado com sucesso.")
    return medico
