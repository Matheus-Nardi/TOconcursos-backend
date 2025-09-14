from pydantic import BaseModel
from datetime import datetime

class ResolucaoQuestaoBaseDTO(BaseModel):
    is_certa: bool
    data_resolucao: datetime | None = None

class ResolucaoQuestaoRequestDTO(ResolucaoQuestaoBaseDTO):
    historico_id: int
    questao_id: int

class ResolucaoQuestaoResponseDTO(ResolucaoQuestaoBaseDTO):
    id: int
    historico_id: int
    questao_id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
