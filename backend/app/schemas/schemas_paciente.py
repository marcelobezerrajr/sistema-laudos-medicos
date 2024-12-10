from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.schemas.schemas_usuario import UsuarioOut

class PacienteBase(BaseModel):
    data_nascimento: date

    class Config:
        from_attributes = True

class PacienteCreate(PacienteBase):
    id_usuario: int

class PacienteUpdate(BaseModel):
    data_nascimento: Optional[date] = None

    class Config:
        from_attributes = True

class PacienteOut(PacienteBase):
    id_paciente: int
    usuario: UsuarioOut

    class Config:
        from_attributes = True
