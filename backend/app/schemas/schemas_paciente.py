from pydantic import BaseModel
from typing import Optional
from app.schemas.schemas_usuario import UsuarioOut
from datetime import datetime

class PacienteBase(BaseModel):
    data_nascimento: datetime

    class Config:
        from_attributes = True

class PacienteCreate(PacienteBase):
    id_usuario: int

class PacienteUpdate(BaseModel):
    data_nascimento: Optional[datetime] = None

    class Config:
        from_attributes = True

class PacienteOut(PacienteBase):
    id_paciente: int
    usuario: UsuarioOut

    class Config:
        from_attributes = True
