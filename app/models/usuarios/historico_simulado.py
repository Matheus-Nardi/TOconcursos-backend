from database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class HistoricoSimulado(Base):
    __tablename__ = "historicos_simulados"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    data_resolucao = Column(DateTime, default=datetime.utcnow, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="historicos_simulados")
    resolucoes = relationship("ResolucaoQuestaoSimulado", back_populates="historico_simulado", cascade="all, delete-orphan")
