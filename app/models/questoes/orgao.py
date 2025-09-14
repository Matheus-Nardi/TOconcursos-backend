from database import Base
from sqlalchemy import Column, Integer, String

class Orgao(Base):
    __tablename__ = "orgaos"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
