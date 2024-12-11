from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.database.models.models_database import Usuario
from app.schemas.schemas_usuario import UsuarioCreate, UsuarioUpdate

logger = logging.getLogger(__name__)

def get_all_usuarios(db: Session):
    usuarios = db.query(Usuario).all()
    if not usuarios:
        logger.warning("Nenhum usuário encontrado.")
    return usuarios

def get_usuario_by_id(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        logger.error(f"Usuário não encontrado com id: {usuario_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

def create_usuario(db: Session, user_form: UsuarioCreate) -> Usuario:
    if db.query(Usuario).filter(Usuario.email == user_form.email).first():
        logger.warning(f"Tentativa de criar um usuário com e-mail existente: {user_form.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado")

    new_user = Usuario(
        nome=user_form.nome,
        email=user_form.email,
        senha_hash=user_form.senha_hash,
        tipo=user_form.tipo,
        data_criacao=user_form.data_criacao
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Usuário {new_user.email} criado com sucesso.")
    return new_user

def update_usuario(db: Session, usuario_id: int, user_form: UsuarioUpdate):
    usuario = get_usuario_by_id(db, usuario_id)

    usuario.nome = user_form.nome or usuario.nome
    usuario.email = user_form.email or usuario.email
    usuario.tipo = user_form.tipo or usuario.tipo

    db.commit()
    db.refresh(usuario)
    logger.info(f"Usuário atualizado com sucesso: {usuario.email}")
    return usuario

def delete_usuario(db: Session, usuario_id: int):
    usuario = get_usuario_by_id(db, usuario_id)
    
    db.delete(usuario)
    db.commit()
    logger.info(f"Usuário deletado com sucesso: {usuario.email}")
    return usuario
