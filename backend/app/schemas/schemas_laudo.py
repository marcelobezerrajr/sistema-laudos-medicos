from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.schemas_medico import MedicoOut
from app.schemas.schemas_exame import ExameOut

class LaudoBase(BaseModel):
    conteudo: str

    class Config:
        from_attributes = True

class LaudoCreate(LaudoBase):
    id_exame: int
    id_medico: int

class LaudoUpdate(BaseModel):
    conteudo: Optional[str] = None

    class Config:
        from_attributes = True

class LaudoOut(LaudoBase):
    id_laudo: int
    data_criacao: datetime
    id_exame: int
    exame: ExameOut
    id_medico: int
    medico: MedicoOut

    class Config:
        from_attributes = True
