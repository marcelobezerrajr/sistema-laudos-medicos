from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import logging

from app.services.services_imagem_exame import create_imagem_exame, get_imagem_exame, list_imagens_por_exame, delete_imagem_exame
from app.api.depends import get_db, get_paciente, get_medico_paciente
from app.schemas.schemas_imagem_exame import ImagemExameOut

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads/exames/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

imagem_exame_router = APIRouter(prefix="/imagens-exame")

@imagem_exame_router.post("/upload", response_model=ImagemExameOut)
async def upload_imagem(id_exame: int, descricao: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_paciente)):
    try:
        file_extension = file.filename.split(".")[-1]
        if file_extension.lower() not in ["jpg", "jpeg", "png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo não permitido. Apenas JPG, JPEG e PNG são aceitos."
            )

        file_path = os.path.join(UPLOAD_DIR, f"exame_{id_exame}_{file.filename}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return create_imagem_exame(db, id_exame, file_path, descricao)
    except Exception as e:
        logger.error(f"Erro ao fazer o upload da imagem do Exame: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao fazer o upload da imagem do Exame")

@imagem_exame_router.get("/view/{id_imagem}", response_model=ImagemExameOut)
def get_imagem(id_imagem: int, db: Session = Depends(get_db), current_user = Depends(get_medico_paciente)):
    try:
        return get_imagem_exame(db, id_imagem)
    except Exception as e:
        logger.error(f"Erro ao listar a imagem do exame: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar a imagem do Exame")

@imagem_exame_router.get("/list/{id_exame}", response_model=List[ImagemExameOut])
def list_imagens_exame(id_exame: int, db: Session = Depends(get_db), current_user = Depends(get_medico_paciente)):
    try:
        return list_imagens_por_exame(db, id_exame)
    except Exception as e:
        logger.error(f"Erro ao listar as imagens do Exame: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar as imagens do Exame")

@imagem_exame_router.delete("/delete/{id_imagem}")
def delete_imagem(id_imagem: int, db: Session = Depends(get_db), current_user = Depends(get_medico_paciente)):
    try:
        return delete_imagem_exame(db, id_imagem)
    except Exception as e:
        logger.error(f"Erro ao deletar a imagem do Exame: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao deletar a imagem do Exame")
