from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
import os

from app.database.models.models_database import ImagemLaudo, Laudo

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/laudos/"


def create_imagem_laudo(db: Session, id_laudo: int, caminho_arquivo: str, descricao: str = None) -> ImagemLaudo:
    laudo = db.query(Laudo).filter(Laudo.id_laudo == id_laudo).first()
    if not laudo:
        logger.error(f"Laudo com ID {id_laudo} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Laudo não encontrado."
        )

    nova_imagem = ImagemLaudo(
        id_laudo=id_laudo,
        caminho_arquivo=caminho_arquivo,
        descricao=descricao,
    )
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)

    logger.info(f"Imagem adicionada ao laudo {id_laudo}: {caminho_arquivo}")
    return nova_imagem


def get_imagem_laudo(db: Session, id_imagem: int) -> ImagemLaudo:
    imagem = db.query(ImagemLaudo).filter(
        ImagemLaudo.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(f"Imagem de laudo com ID {id_imagem} não encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem de laudo não encontrada."
        )
    return imagem


def list_imagens_por_laudo(db: Session, id_laudo: int) -> list[ImagemLaudo]:
    imagens = db.query(ImagemLaudo).filter(
        ImagemLaudo.id_laudo == id_laudo).all()
    if not imagens:
        logger.warning(f"Nenhuma imagem encontrada para o laudo {id_laudo}.")
    return imagens


def delete_imagem_laudo(db: Session, id_imagem: int):
    imagem = db.query(ImagemLaudo).filter(
        ImagemLaudo.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(f"Imagem de laudo com ID {
                     id_imagem} não encontrada para exclusão.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem de laudo não encontrada para exclusão."
        )

    if os.path.exists(imagem.caminho_arquivo):
        os.remove(imagem.caminho_arquivo)
        logger.info(f"Arquivo físico {
                    imagem.caminho_arquivo} removido com sucesso.")

    db.delete(imagem)
    db.commit()
    logger.info(f"Imagem de laudo com ID {
                id_imagem} deletada do banco de dados.")
    return {"detail": "Imagem de laudo deletada com sucesso."}
