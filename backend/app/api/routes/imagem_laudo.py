from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import logging

from app.services.services_imagem_laudo import create_imagem_laudo, get_imagem_laudo, list_imagens_por_laudo, delete_imagem_laudo
from app.api.depends import get_db, get_medico, get_medico_paciente
from app.schemas.schemas_imagem_laudo import ImagemLaudoOut

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/laudos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

imagem_laudo_router = APIRouter(prefix="/imagens-laudo")


@imagem_laudo_router.post("/upload", response_model=ImagemLaudoOut)
async def upload_imagem_laudo(id_laudo: int, descricao: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_medico)):
    try:
        file_extension = file.filename.split(".")[-1]
        if file_extension.lower() not in ["jpg", "jpeg", "png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo não permitido. Apenas JPG, JPEG e PNG são aceitos."
            )

        file_path = os.path.join(UPLOAD_DIR, f"laudo_{
                                 id_laudo}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return create_imagem_laudo(db, id_laudo, file_path, descricao)
    except Exception as e:
        logger.error(f"Erro ao fazer o upload da imagem do Laudo: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao fazer o upload da imagem do Laudo")


@imagem_laudo_router.get("/{id_imagem}", response_model=ImagemLaudoOut)
def get_imagem_laudo(id_imagem: int, db: Session = Depends(get_db), current_user=Depends(get_medico_paciente)):
    try:
        return get_imagem_laudo(db, id_imagem)
    except Exception as e:
        logger.error(f"Erro ao listar a imagem do Laudo: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao listar a imagem do Laudo")


@imagem_laudo_router.get("/list/{id_laudo}", response_model=List[ImagemLaudoOut])
def list_imagens_laudo(id_laudo: int, db: Session = Depends(get_db), current_user=Depends(get_medico_paciente)):
    try:
        return list_imagens_por_laudo(db, id_laudo)
    except Exception as e:
        logger.error(f"Erro ao listar as imagens do Laudo: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao listar a imagens do Laudo")


@imagem_laudo_router.delete("/delete/{id_imagem}")
def delete_imagem_laudo(id_imagem: int, db: Session = Depends(get_db), current_user=Depends(get_medico_paciente)):
    try:
        return delete_imagem_laudo(db, id_imagem)
    except Exception as e:
        logger.error(f"Erro ao deletar a imagem do Laudo: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao deletar a imagem do Laudo")
