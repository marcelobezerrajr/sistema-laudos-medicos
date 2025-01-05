from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Paciente, Usuario
from app.schemas.schemas_paciente import PacienteCreate, PacienteUpdate

logger = logging.getLogger(__name__)


def get_all_pacientes(db: Session):
    pacientes = db.query(Paciente).all()
    if not pacientes:
        logger.warning("Nenhum paciente encontrado.")
    return pacientes


def get_paciente_by_id(db: Session, paciente_id: int):
    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == paciente_id).first()
    if not paciente:
        logger.error(f"Paciente não encontrado com id: {paciente_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Paciente não encontrado")
    return paciente


def create_paciente(db: Session, paciente_data: PacienteCreate):
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == paciente_data.id_usuario).first()
    if not usuario:
        logger.error(f"Usuário não encontrado com id: {
                     paciente_data.id_usuario}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")

    if usuario.tipo != 'paciente':
        logger.error(f"Usuário com o id: {
                     paciente_data.id_usuario} não é paciente, operação não permitida.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário não é paciente")

    new_paciente = Paciente(
        id_paciente=paciente_data.id_usuario,
        data_nascimento=paciente_data.data_nascimento,
    )

    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    logger.info(f"Paciente com o id {
                new_paciente.id_paciente} criado com sucesso!")
    return new_paciente


def update_paciente(db: Session, paciente_id: int, paciente_data: PacienteUpdate):
    paciente = get_paciente_by_id(db, paciente_id)

    paciente.data_nascimento = paciente_data.data_nascimento or paciente.data_nascimento

    db.commit()
    db.refresh(paciente)
    logger.info(f"Médico com id {paciente_id} atualizado com sucesso.")
    return paciente


def delete_paciente(db: Session, paciente_id: int):
    paciente = get_paciente_by_id(db, paciente_id)

    db.delete(paciente)
    db.commit()
    logger.info(f"Paciente com id {paciente_id} deletado com sucesso.")
    return paciente
