from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Usuario
from app.schemas.schemas_usuario import UsuarioCreate, UsuarioUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_usuarios(db: Session):
    logger.info("Buscando todos os usuários.")
    usuarios = db.query(Usuario).all()
    if not usuarios:
        logger.warning("Nenhum usuário encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum usuário encontrado"
        )
    return usuarios


def get_usuario_by_id(db: Session, usuario_id: int):
    logger.info(f"Buscando usuário com ID {usuario_id}.")
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        logger.warning(f"Usuário com o ID {usuario_id} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com o ID {usuario_id} não encontrado.",
        )
    return usuario


def create_usuario(db: Session, user_form: UsuarioCreate) -> Usuario:
    logger.info(f"Criando usuário {user_form.nome}.")
    if db.query(Usuario).filter(Usuario.email == user_form.email).first():
        logger.warning(
            f"Tentativa de criar um usuário com e-mail existente: {user_form.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado"
        )

    new_user = Usuario(
        nome=user_form.nome,
        email=user_form.email,
        senha_hash=user_form.senha_hash,
        tipo=user_form.tipo,
        data_criacao=user_form.data_criacao,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Usuário {user_form.nome} criado com sucesso.")
    return new_user


def update_usuario(db: Session, usuario_id: int, user_form: UsuarioUpdate):
    logger.info(f"Atualizando usuário com o ID {usuario_id}.")
    usuario = get_usuario_by_id(db, usuario_id)

    usuario.nome = user_form.nome or usuario.nome
    usuario.email = user_form.email or usuario.email
    usuario.tipo = user_form.tipo or usuario.tipo

    db.commit()
    db.refresh(usuario)
    logger.info(f"Usuário com o ID {usuario_id} atualizado com sucesso.")
    return usuario


def delete_usuario(db: Session, usuario_id: int):
    logger.info(f"Deletando usuário com o ID {usuario_id}.")
    usuario = get_usuario_by_id(db, usuario_id)

    db.delete(usuario)
    db.commit()
    logger.info(f"Usuário com ID {usuario_id} deletado com sucesso do banco de dados.")
    return usuario
