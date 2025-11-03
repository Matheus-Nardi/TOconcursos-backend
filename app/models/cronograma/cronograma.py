from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from models.cronograma.dia_da_semana import DiaDaSemanaEnum 
from datetime import time

class Cronograma(Base):
    __tablename__ = "cronogramas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    estudos_diarios = relationship("EstudoDiario", cascade="all, delete-orphan")

   
    usuario_id = Column(Integer, ForeignKey("usuarios.id")) 

    usuario = relationship("Usuario", back_populates="cronogramas")
