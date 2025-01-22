from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

from app.database.models.models_database import Tipo_Usuario
from app.utils.hashing_senha import get_password_hash
from app.utils.validate_senha import validate_password


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    senha_hash: str
    tipo: Tipo_Usuario
    data_criacao: datetime

    class Config:
        from_attributes = True

    @validator("nome")
    def validate_nome(cls, value):
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", value):
            raise ValueError("Nome está no formato inválido")
        return value

    @validator("senha_hash", pre=True)
    def validate_and_hash_password(cls, value):
        validate_password(value)
        return get_password_hash(value)


class UsuarioListResponse(BaseModel):
    nome: str
    email: EmailStr
    tipo: Tipo_Usuario
    data_criacao: datetime


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo: Optional[Tipo_Usuario] = None

    class Config:
        from_attributes = True

    @validator("nome", pre=True, always=True)
    def validate_nome(cls, value):
        if value and not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", value):
            raise ValueError("Nome está no formato inválido")
        return value


class UsuarioOut(UsuarioListResponse):
    id_usuario: int

    class Config:
        from_attributes = True


class MensagemResposta(BaseModel):
    message: str
