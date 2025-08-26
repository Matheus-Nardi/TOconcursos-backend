from database import Base
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cpf = Column(String, unique=True, nullable=False, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    avatar = Column(String, nullable=True)
    senha = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
