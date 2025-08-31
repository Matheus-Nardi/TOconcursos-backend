from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, Time
from sqlalchemy.orm import relationship
from models.cronograma.dia_da_semana import DiaDaSemanaEnum 
from datetime import time

class EstudoDiario(Base):
    __tablename__ = "estudos_diarios"

    id = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    concluido = Column(Boolean, default=False)
    dia_da_semana = Column(Enum(DiaDaSemanaEnum), nullable=False, default=DiaDaSemanaEnum.SEGUNDA)
    id_disciplina = Column(Integer, ForeignKey("disciplinas.id"))
    disciplina = relationship("Disciplina")

    id_cronograma = Column(Integer, ForeignKey("cronogramas.id"))
    cronograma = relationship("Cronograma")
