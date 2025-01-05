from pydantic import BaseModel
from typing import Optional


class ImagemLaudoBase(BaseModel):
    id_laudo: int
    descricao: Optional[str] = None

    class Config:
        from_attributes = True


class ImagemLaudoCreate(ImagemLaudoBase):
    caminho_arquivo: str


class ImagemLaudoOut(ImagemLaudoBase):
    id_imagem: int
    caminho_arquivo: str

    class Config:
        from_attributes = True
