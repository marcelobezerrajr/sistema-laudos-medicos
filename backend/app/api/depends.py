from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database.database import SessionLocal
from app.database.models.models_database import Usuario, Tipo_Usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_usuario(id_usuario: int, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if usuario is None:
        logger.warning(f"Usuário com ID {id_usuario} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com o ID {id_usuario} não encontrado",
        )
    return usuario


def check_usuario_role(
    usuario: Usuario,
    roles_permitidos: list[Tipo_Usuario],
    mensagem_erro: str = "Permissões insuficientes.",
) -> Usuario:
    if usuario.tipo not in roles_permitidos:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=mensagem_erro)
    return usuario


def get_medico(current_user: Usuario = Depends(get_current_usuario)) -> Usuario:
    return check_usuario_role(
        current_user,
        roles_permitidos=[Tipo_Usuario.medico],
        mensagem_erro="Acesso permitido apenas para médicos.",
    )


def get_paciente(current_user: Usuario = Depends(get_current_usuario)) -> Usuario:
    return check_usuario_role(
        current_user,
        roles_permitidos=[Tipo_Usuario.paciente],
        mensagem_erro="Acesso permitido apenas para pacientes.",
    )


def get_medico_paciente(
    current_user: Usuario = Depends(get_current_usuario),
) -> Usuario:
    return check_usuario_role(
        current_user,
        roles_permitidos=[Tipo_Usuario.medico, Tipo_Usuario.paciente],
        mensagem_erro="Acesso permitido apenas para médicos e pacientes.",
    )
