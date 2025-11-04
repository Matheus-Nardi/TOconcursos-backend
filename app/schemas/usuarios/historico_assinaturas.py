from pydantic import BaseModel
from datetime import datetime
from schemas.planos.plano import PlanoResponseDTO, PlanoSimplificadoDTO

class HistoricoAssinaturasDTO(BaseModel):
    """DTO contendo o plano atual e histórico de assinaturas do usuário."""
    plano_atual: PlanoSimplificadoDTO | None = None
    historico_assinaturas: list[PlanoSimplificadoDTO] = []

    class Config:
        from_attributes = True
    