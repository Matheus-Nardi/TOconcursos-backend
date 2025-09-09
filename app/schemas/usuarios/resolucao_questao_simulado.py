from pydantic import BaseModel
from datetime import datetime

class ResolucaoQuestaoSimuladoBaseDTO(BaseModel):
    historico_simulado_id: int
    questao_id: int
    correta: bool


class ResolucaoQuestaoSimuladoRequestDTO(ResolucaoQuestaoSimuladoBaseDTO):
    pass

class ResolucaoQuestaoSimuladoResponseDTO(ResolucaoQuestaoSimuladoBaseDTO):
    id: int
    data_resolucao: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
