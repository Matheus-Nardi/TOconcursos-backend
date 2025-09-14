from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Historico(Base):
    __tablename__ = "historicos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    dias_sequencia = Column(Integer, nullable=False, default=0)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="historicos")
    resolucoes = relationship("ResolucaoQuestao", back_populates="historico", cascade="all, delete-orphan")

