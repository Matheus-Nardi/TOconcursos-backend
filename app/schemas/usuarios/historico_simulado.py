from pydantic import BaseModel
from datetime import datetime

class HistoricoSimuladoBaseDTO(BaseModel):
    data_resolucao: datetime | None = None

class HistoricoSimuladoRequestDTO(HistoricoSimuladoBaseDTO):
    usuario_id: int

class HistoricoSimuladoResponseDTO(HistoricoSimuladoBaseDTO):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
