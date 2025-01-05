from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
import os

from app.database.models.models_database import ImagemExame, Exame

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/exames/"


def create_imagem_exame(db: Session, id_exame: int, caminho_arquivo: str, descricao: str = None) -> ImagemExame:
    exame = db.query(Exame).filter(Exame.id_exame == id_exame).first()
    if not exame:
        logger.error(f"Exame com ID {id_exame} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exame não encontrado."
        )

    nova_imagem = ImagemExame(
        id_exame=id_exame,
        caminho_arquivo=caminho_arquivo,
        descricao=descricao,
    )
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)

    logger.info(f"Imagem adicionada ao exame {id_exame}: {caminho_arquivo}")
    return nova_imagem


def get_imagem_exame(db: Session, id_imagem: int) -> ImagemExame:
    imagem = db.query(ImagemExame).filter(
        ImagemExame.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(f"Imagem com ID {id_imagem} não encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem não encontrada."
        )
    return imagem


def list_imagens_por_exame(db: Session, id_exame: int) -> list[ImagemExame]:
    imagens = db.query(ImagemExame).filter(
        ImagemExame.id_exame == id_exame).all()
    if not imagens:
        logger.warning(f"Nenhuma imagem encontrada para o exame {id_exame}.")
    return imagens


def delete_imagem_exame(db: Session, id_imagem: int):
    imagem = db.query(ImagemExame).filter(
        ImagemExame.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(f"Imagem com ID {
                     id_imagem} não encontrada para exclusão.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem não encontrada para exclusão."
        )

    if os.path.exists(imagem.caminho_arquivo):
        os.remove(imagem.caminho_arquivo)
        logger.info(f"Arquivo físico {
                    imagem.caminho_arquivo} removido com sucesso.")

    db.delete(imagem)
    db.commit()
    logger.info(f"Imagem com ID {id_imagem} deletada do banco de dados.")
    return {"detail": "Imagem deletada com sucesso."}
