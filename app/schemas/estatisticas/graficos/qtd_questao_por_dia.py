from pydantic import BaseModel
from datetime import datetime



class QuantidadeQuestoesPorDia(BaseModel):
    data: datetime
    quantidade_questoes: int

    class Config:
        from_attributes = True
    