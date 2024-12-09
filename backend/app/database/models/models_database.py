from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(Enum('medico', 'paciente', name='tipo_usuario'), nullable=False)
    data_criacao = Column(TIMESTAMP, default=func.now())
    medico = relationship("Medico", back_populates="usuario", uselist=False)
    paciente = relationship("Paciente", back_populates="usuario", uselist=False)

class Medico(Base):
    __tablename__ = 'medicos'

    id_medico = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True)
    especialidade = Column(String(255), nullable=False)
    crm = Column(String(50), unique=True, nullable=False)
    usuario = relationship("Usuario", back_populates="medico")
    laudos = relationship("Laudo", back_populates="medico")

class Paciente(Base):
    __tablename__ = 'pacientes'

    id_paciente = Column(Integer, ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True)
    data_nascimento = Column(Date, nullable=False)
    usuario = relationship("Usuario", back_populates="paciente")
    exames = relationship("Exame", back_populates="paciente")

class Exame(Base):
    __tablename__ = 'exames'

    id_exame = Column(Integer, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id_paciente', ondelete='CASCADE'), nullable=False)
    tipo_exame = Column(String(255), nullable=False)
    data_envio = Column(TIMESTAMP, default=func.now(), nullable=False)
    status = Column(Enum('pendente', 'em_analise', 'concluido', name='status_exame'), default='pendente', nullable=False)
    paciente = relationship("Paciente", back_populates="exames")
    imagens = relationship("ImagemExame", back_populates="exame")
    laudo = relationship("Laudo", back_populates="exame", uselist=False)

class ImagemExame(Base):
    __tablename__ = 'imagens_exame'

    id_imagem = Column(Integer, primary_key=True, autoincrement=True)
    id_exame = Column(Integer, ForeignKey('exames.id_exame', ondelete='CASCADE'), nullable=False)
    caminho_arquivo = Column(String(255), nullable=False)  # Localização do arquivo
    descricao = Column(String(255))
    exame = relationship("Exame", back_populates="imagens")

class Laudo(Base):
    __tablename__ = 'laudos'

    id_laudo = Column(Integer, primary_key=True, autoincrement=True)
    id_exame = Column(Integer, ForeignKey('exames.id_exame', ondelete='CASCADE'), nullable=False)
    id_medico = Column(Integer, ForeignKey('medicos.id_medico', ondelete='CASCADE'), nullable=False)
    conteudo = Column(Text, nullable=False)
    data_criacao = Column(TIMESTAMP, default=func.now(), nullable=False)
    exame = relationship("Exame", back_populates="laudo")
    medico = relationship("Medico", back_populates="laudos")
