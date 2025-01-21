from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
import os

from app.database.models.models_database import ImagemLaudo, Laudo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_imagem_laudo(
    db: Session, id_laudo: int, caminho_arquivo: str, descricao: str = None
) -> ImagemLaudo:
    logger.info(f"Criando imagem para laudo {id_laudo}.")
    laudo = db.query(Laudo).filter(Laudo.id_laudo == id_laudo).first()
    if not laudo:
        logger.error(f"Laudo com o ID {id_laudo} não encontrado.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laudo com o ID {id_laudo} não encontrado.",
        )

    nova_imagem = ImagemLaudo(
        id_laudo=id_laudo,
        caminho_arquivo=caminho_arquivo,
        descricao=descricao,
    )
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)

    logger.info(
        f"Imagem criada com sucesso para laudo {id_laudo}. ID: {nova_imagem.id_imagem}"
    )
    return nova_imagem


def get_imagem_laudo(db: Session, id_imagem: int) -> ImagemLaudo:
    logger.info(f"Obtendo imagem com ID {id_imagem}.")
    imagem = db.query(ImagemLaudo).filter(ImagemLaudo.id_imagem == id_imagem).first()
    if not imagem:
        logger.warning(f"Imagem com ID {id_imagem} não encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem de laudo com o ID {id_imagem} não encontrada.",
        )
    logger.info(f"Imagem com ID {id_imagem} encontrada.")
    return imagem


def list_imagens_por_laudo(db: Session, id_laudo: int) -> list[ImagemLaudo]:
    logger.info(f"Listando imagens para laudo {id_laudo}.")
    imagens = db.query(ImagemLaudo).filter(ImagemLaudo.id_laudo == id_laudo).all()
    if not imagens:
        logger.warning(f"Nenhuma imagem encontrada para laudo {id_laudo}.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum imagem encontrada para o laudo {id_laudo}.",
        )
    logger.info(f"Foram encontradas imagens {len(imagens)} para o Laudo {id_laudo}.")
    return imagens


def delete_imagem_laudo(db: Session, id_imagem: int):
    logger.info(f"Deletando imagem com o ID {id_imagem}.")
    imagem = db.query(ImagemLaudo).filter(ImagemLaudo.id_imagem == id_imagem).first()
    if not imagem:
        logger.error(
            f"Imagem de laudo com ID {id_imagem} não encontrada para exclusão."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagem de laudo com ID {id_imagem} não encontrada para exclusão.",
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
    logger.info(f"Imagem de laudo com ID {id_imagem} deletada do banco de dados.")
    return {"detail": "Imagem de laudo deletada com sucesso."}
