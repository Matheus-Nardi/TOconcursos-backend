from pydantic import BaseModel
from datetime import datetime
from schemas.planos.plano import PlanoResponseDTO

class HistoricoAssinaturasDTO(BaseModel):
    """DTO contendo o plano atual e histórico de assinaturas do usuário."""
    plano_atual: PlanoResponseDTO | None = None
    historico_assinaturas: list[PlanoResponseDTO] = []

    class Config:
        from_attributes = True
    