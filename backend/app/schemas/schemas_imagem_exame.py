from pydantic import BaseModel
from typing import Optional


class ImagemExameBase(BaseModel):
    id_exame: int
    descricao: Optional[str] = None

    class Config:
        from_attributes = True


class ImagemExameCreate(ImagemExameBase):
    caminho_arquivo: str


class ImagemExameOut(ImagemExameBase):
    id_imagem: int
    caminho_arquivo: str

    class Config:
        from_attributes = True
