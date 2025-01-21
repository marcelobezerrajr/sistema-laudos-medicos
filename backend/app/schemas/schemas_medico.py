from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.schemas_usuario import UsuarioOut


class MedicoBase(BaseModel):
    especialidade: str
    crm: str = Field(..., pattern=r"^\d{6}$")

    class Config:
        from_attributes = True


class MedicoCreate(MedicoBase):
    id_usuario: int


class MedicoUpdate(BaseModel):
    especialidade: Optional[str] = None
    crm: Optional[str] = None

    class Config:
        from_attributes = True


class MedicoOut(MedicoBase):
    id_medico: int
    usuario: UsuarioOut

    class Config:
        from_attributes = True
