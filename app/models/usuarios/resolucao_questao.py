from database import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime

class ResolucaoQuestao(Base):
    __tablename__ = "resolucoes_questoes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    data_resolucao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_certa = Column(Boolean, nullable=False)

    questao_id = Column(Integer, ForeignKey("questoes.id"), nullable=False)
    questao = relationship("Questao", back_populates="resolucoes")


    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="resolucoes_questoes")
    # Removido o relacionamento com Historico
    # historico_id = Column(Integer, ForeignKey("historicos.id"), nullable=False)
    # historico = relationship("Historico", back_populates="resolucoes")
