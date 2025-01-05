from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, TIMESTAMP, func, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.database.database import Base


class Tipo_Usuario(str, PyEnum):
    medico = "medico"
    paciente = "paciente"


class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(SqlEnum(Tipo_Usuario),
                  default=Tipo_Usuario.paciente, nullable=False)
    data_criacao = Column(TIMESTAMP, default=func.now(), nullable=False)

    medico = relationship("Medico", back_populates="usuario", uselist=False)
    paciente = relationship(
        "Paciente", back_populates="usuario", uselist=False)


class Medico(Base):
    __tablename__ = 'medicos'

    id_medico = Column(Integer, ForeignKey(
        'usuarios.id_usuario', ondelete='CASCADE'), primary_key=True)
    especialidade = Column(String(255), nullable=False)
    crm = Column(String(50), unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="medico")
    laudos = relationship("Laudo", back_populates="medico")


class Paciente(Base):
    __tablename__ = 'pacientes'

    id_paciente = Column(Integer, ForeignKey(
        'usuarios.id_usuario', ondelete='CASCADE'), primary_key=True)
    data_nascimento = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="paciente")
    exames = relationship("Exame", back_populates="paciente")


class Status_Exame(str, PyEnum):
    pendente = "pendente"
    em_analise = "em_analise"
    concluido = "concluido"


class Exame(Base):
    __tablename__ = 'exames'

    id_exame = Column(Integer, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey(
        'pacientes.id_paciente', ondelete='CASCADE'), nullable=False)
    tipo_exame = Column(String(255), nullable=False)
    data_envio = Column(TIMESTAMP, default=func.now(), nullable=False)
    status = Column(SqlEnum(Status_Exame),
                    default=Status_Exame.pendente, nullable=False)

    paciente = relationship("Paciente", back_populates="exames")
    imagens = relationship("ImagemExame", back_populates="exame")
    laudo = relationship("Laudo", back_populates="exame", uselist=False)


class ImagemExame(Base):
    __tablename__ = 'imagens_exame'

    id_imagem = Column(Integer, primary_key=True, autoincrement=True)
    id_exame = Column(Integer, ForeignKey(
        'exames.id_exame', ondelete='CASCADE'), nullable=False)
    caminho_arquivo = Column(String(255), nullable=False)
    descricao = Column(String(255))

    exame = relationship("Exame", back_populates="imagens")


class Laudo(Base):
    __tablename__ = 'laudos'

    id_laudo = Column(Integer, primary_key=True, autoincrement=True)
    id_exame = Column(Integer, ForeignKey(
        'exames.id_exame', ondelete='CASCADE'), nullable=False)
    id_medico = Column(Integer, ForeignKey(
        'medicos.id_medico', ondelete='CASCADE'), nullable=False)
    conteudo = Column(Text, nullable=False)
    data_criacao = Column(TIMESTAMP, default=func.now(), nullable=False)

    exame = relationship("Exame", back_populates="laudo")
    medico = relationship("Medico", back_populates="laudos")
    imagens = relationship("ImagemLaudo", back_populates="laudo")


class ImagemLaudo(Base):
    __tablename__ = 'imagens_laudo'

    id_imagem = Column(Integer, primary_key=True, autoincrement=True)
    id_laudo = Column(Integer, ForeignKey(
        'laudos.id_laudo', ondelete='CASCADE'), nullable=False)
    caminho_arquivo = Column(String(255), nullable=False)
    descricao = Column(String(255))

    laudo = relationship("Laudo", back_populates="imagens")
