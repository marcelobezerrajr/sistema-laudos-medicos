from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database.database import SessionLocal
from app.database.models.models_database import Usuario, Tipo_Usuario

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_usuario(usuario_id: int, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        logger.warning(f"Usuário com ID {usuario_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario

def get_medico(current_user: Usuario = Depends(get_current_usuario)) -> Usuario:
    if current_user.tipo != Tipo_Usuario.medico:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes: acesso permitido apenas para médicos."
        )
    return current_user

def get_paciente(current_user: Usuario = Depends(get_current_usuario)) -> Usuario:
    if current_user.tipo != Tipo_Usuario.paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes: acesso permitido apenas para pacientes."
        )
    return current_user

def get_medico_paciente(current_user: Usuario = Depends(get_current_usuario)) -> Usuario:
    if current_user.tipo not in [Tipo_Usuario.medico, Tipo_Usuario.paciente]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes: acesso permitido apenas para médicos e pacientes."
        )
    return current_user
