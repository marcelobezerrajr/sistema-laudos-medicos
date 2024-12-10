from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database.models.models_database import Status_Exame
from app.schemas.schemas_paciente import PacienteOut

class ExameBase(BaseModel):
    tipo_exame: str
    status: Status_Exame

    class Config:
        from_attributes = True

class ExameCreate(ExameBase):
    id_paciente: int

class ExameUpdate(BaseModel):
    tipo_exame: Optional[str] = None
    status: Optional[Status_Exame] = None

    class Config:
        from_attributes = True

class ExameOut(ExameBase):
    id_exame: int
    id_paciente: int
    data_envio: datetime
    paciente: PacienteOut

    class Config:
        from_attributes = True
