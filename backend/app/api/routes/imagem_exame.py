from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
import shutil
import os

from app.services.services_imagem_exame import (
    create_imagem_exame,
    get_imagem_exame,
    list_imagens_por_exame,
    delete_imagem_exame,
)
from app.database.models.models_database import Usuario
from app.schemas.schemas_imagem_exame import ImagemExameOut
from app.api.depends import get_db, get_paciente, get_medico_paciente

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "sistema-laudos-medicos/uploads/exames/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

imagem_exame_router = APIRouter(prefix="/imagens-exame")


@imagem_exame_router.post("/upload", response_model=ImagemExameOut)
async def upload_imagem(
    id_exame: int,
    descricao: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_paciente),
):
    logger.info(
        f"O paciente {current_user.nome} está fazendo upload da imagem do exame com o ID {id_exame}."
    )
    try:
        file_extension = file.filename.split(".")[-1]
        if file_extension.lower() not in ["jpg", "jpeg", "png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de arquivo não permitido. Apenas JPG, JPEG e PNG são aceitos.",
            )

        file_path = os.path.join(
            UPLOAD_DIR,
            f"exame_{id_exame}_{file.filename}",
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return create_imagem_exame(db, id_exame, file_path, descricao)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer o upload da imagem do Exame - {str(e)}",
        )


@imagem_exame_router.get("/view/{id_imagem}", response_model=ImagemExameOut)
def get_imagem(
    id_imagem: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_medico_paciente),
):
    logger.info(
        f"O usuário {current_user.nome} está visualizando a imagem do exame com o ID {id_imagem}."
    )
    try:
        return get_imagem_exame(db, id_imagem)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar a imagem do Exame - {str(e)}"
        )


@imagem_exame_router.get("/list/{id_exame}", response_model=List[ImagemExameOut])
def list_imagens_exame(
    id_exame: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_medico_paciente),
):
    logger.info(
        f"O usuário {current_user.nome} está listando as imagens do exame com o ID {id_exame}."
    )
    try:
        return list_imagens_por_exame(db, id_exame)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar as imagens do Exame - {str(e)}"
        )


@imagem_exame_router.delete("/delete/{id_imagem}")
def delete_imagem(
    id_imagem: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_medico_paciente),
):
    logger.info(
        f"O usuário {current_user.nome} está excluindo a imagem do exame com ID {id_imagem}."
    )
    try:
        return delete_imagem_exame(db, id_imagem)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar a imagem do Exame - {str(e)}"
        )
