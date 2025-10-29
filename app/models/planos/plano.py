from database import Base
from sqlalchemy import Column, JSON, String, DateTime, Integer, Numeric

from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import relationship

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    valor = Column(Numeric(precision=10, scale=2), nullable=False)
    beneficios = Column(JSON, nullable=False)