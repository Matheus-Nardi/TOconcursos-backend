from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from schemas.planos.plano import PlanoResponseDTO, PlanoSimplificadoDTO

class PlanoComDataAssinaturaDTO(BaseModel):
    """DTO contendo um plano, a data em que foi assinado e o método de pagamento."""
    plano: PlanoSimplificadoDTO
    data_assinatura: datetime
    metodo_pagamento: Literal["pix", "boleto", "cartao"]

    class Config:
        from_attributes = True

class HistoricoAssinaturasDTO(BaseModel):
    """DTO contendo o plano atual e histórico de assinaturas do usuário."""
    plano_atual: PlanoSimplificadoDTO | None = None
    historico_assinaturas: list[PlanoComDataAssinaturaDTO] = []

    class Config:
        from_attributes = True
    