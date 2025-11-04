from pydantic import BaseModel
from datetime import datetime
from schemas.questoes.questao import QuestaoSimplificadaResponseDTO


class ResolucaoQuestaoBaseDTO(BaseModel):
    is_certa: bool
   

class ResolucaoQuestaoRequestDTO(ResolucaoQuestaoBaseDTO):
    questao_id: int

class ResolucaoQuestaoResponseDTO(ResolucaoQuestaoBaseDTO):
    id: int
    questao: QuestaoSimplificadaResponseDTO
    data_resolucao: datetime | None = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}
