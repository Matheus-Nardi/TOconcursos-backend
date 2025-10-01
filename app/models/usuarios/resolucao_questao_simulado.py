from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class ResolucaoQuestaoSimulado(Base):
    __tablename__ = "resolucoes_questoes_simulados"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    historico_simulado_id = Column(Integer, ForeignKey("historicos_simulados.id"), nullable=False)
    questao_id = Column(Integer, ForeignKey("questoes.id"), nullable=False)
    correta = Column(Boolean, nullable=False)
    data_resolucao = Column(DateTime, default=datetime.utcnow)

    historico_simulado = relationship("HistoricoSimulado", back_populates="resolucoes")
    questao = relationship("Questao")
