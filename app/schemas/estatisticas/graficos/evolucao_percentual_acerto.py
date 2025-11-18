from pydantic import BaseModel
from datetime import datetime

class EvolucaoPercentualAcerto(BaseModel):
    data: datetime
    percentual_acerto: float
    total_questoes: int

    class Config:
        from_attributes = True

