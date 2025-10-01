from database import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ResolucaoQuestao(Base):
    __tablename__ = "resolucoes_questoes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    data_resolucao = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_certa = Column(Boolean, nullable=False)

    historico_id = Column(Integer, ForeignKey("historicos.id"), nullable=False)
    questao_id = Column(Integer, ForeignKey("questoes.id"), nullable=False)

    historico = relationship("Historico", back_populates="resolucoes")
    questao = relationship("Questao", back_populates="resolucoes")
