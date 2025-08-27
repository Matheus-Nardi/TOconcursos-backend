from database import Base
from sqlalchemy import Column, Integer, String

class Banca(Base):
    __tablename__ = "bancas"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)