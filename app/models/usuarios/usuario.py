from database import Base
from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cpf = Column(String, unique=True, nullable=False, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    avatar = Column(String, nullable=True)
    senha = Column(String, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    comentarios = relationship("Comentario", back_populates="usuario")

    cronogramas = relationship("Cronograma", back_populates="usuario", cascade="all, delete-orphan")

    pagamentos = relationship("Pagamento", back_populates="usuario", cascade="all, delete-orphan")

    resolucoes_questoes = relationship("ResolucaoQuestao", back_populates="usuario", cascade="all, delete-orphan")