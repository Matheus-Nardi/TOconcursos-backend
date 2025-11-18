from pydantic import BaseModel
from datetime import datetime



class QuantidadeCertoErradoPorDia(BaseModel):
    data: datetime
    quantidade_questoes_certas: int
    quantidade_questoes_erradas: int

    class Config:
        from_attributes = True
    