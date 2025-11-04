from pydantic import BaseModel
from datetime import datetime
from schemas.planos.plano import PlanoResponseDTO

class EstatisticasUsuarioDTO(BaseModel):
    """DTO contendo estatísticas de uso e progresso do usuário."""
    total_questoes_resolvidas: int = 0
    total_acertos: int = 0
    total_erros: int = 0
    percentual_acerto: float = 0.0
    total_cronogramas: int = 0
    dias_consecutivos_estudo: int = 0  # Streak
    ultima_atividade: datetime | None = None

    class Config:
        from_attributes = True
    