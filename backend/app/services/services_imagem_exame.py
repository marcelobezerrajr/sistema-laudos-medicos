from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
import os

from app.database.models.models_database import ImagemExame, Exame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_imagem_exame(
    db: Session, id_exame: int, caminho_arquivo: str, descricao: str = None
) -> ImagemExame:
    logger.info(f"Criando imagem para exame {id_exame}.")
    exame = db.query(Exame).filter(Exame.id_exame == id_exame).first()
    if not exame:
        logger.error(f"Imagem com o ID {id_exame} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exame com o ID {id_exame} não encontrado.",
        )

    nova_imagem = ImagemExame(
        id_exame=id_exame,
        caminho_arquivo=caminho_arquivo,
        descricao=descricao,
    )
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)

    logger.info(
        f"Imagem criada com sucesso para o exame {id_exame}. ID: {nova_imagem.id_imagem}"
    )
    return nova_imagem


def get_imagem_exame(db: Session, id_imagem: int) -> ImagemExame:
    logger.info(f"Obtendo imagem com ID {id_imagem}.")
    imagem = db.query(ImagemExame).filter(ImagemExame.id_imagem == id_imagem).first()
    if not imagem:
        logger.warning(f"Imagem com ID {id_imagem} não encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem com o ID {id_imagem} não encontrada.",
        )
    logger.info(f"Imagem com ID {id_imagem} encontrada.")
    return imagem


def list_imagens_por_exame(db: Session, id_exame: int) -> list[ImagemExame]:
    logger.info(f"Listando imagens para exame {id_exame}.")
    imagens = db.query(ImagemExame).filter(ImagemExame.id_exame == id_exame).all()
    if not imagens:
        logger.warning(f"Nenhuma imagem encontrada para exame {id_exame}.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum imagem encontrada para o exame {id_exame}.",
        )
    logger.info(f"Foram encontradas imagens {len(imagens)} para o Exame {id_exame}.")
    return imagens


def delete_imagem_exame(db: Session, id_imagem: int):
    logger.info(f"Deletando imagem com o ID {id_imagem}.")
    imagem = db.query(ImagemExame).filter(ImagemExame.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(
            f"Imagem de exame com ID {id_imagem} não encontrada para exclusão."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem com o ID {id_imagem} não encontrada para exclusão.",
        )

    if os.path.exists(imagem.caminho_arquivo):
        logger.info(f"Arquivo {imagem.caminho_arquivo} existe. Removendo.")
        os.remove(imagem.caminho_arquivo)
    else:
        logger.warning(
            f"Arquivo {imagem.caminho_arquivo} não encontrado. Ignorando remoção."
        )

    db.delete(imagem)
    db.commit()
    logger.info(f"Imagem de exame com ID {id_imagem} deletada do banco de dados.")
    return {"detail": "Imagem deletada com sucesso."}
