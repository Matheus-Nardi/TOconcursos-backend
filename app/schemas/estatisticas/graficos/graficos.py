from pydantic import BaseModel
from datetime import datetime
from typing import List
from .qtd_questao_por_dia import QuantidadeQuestoesPorDia
from .qtd_certo_errado_questao_por_dia import QuantidadeCertoErradoPorDia

class GraficosResponseDTO(BaseModel):
    quantidade_questoes_por_dia: List[QuantidadeQuestoesPorDia]
    quantidade_certo_errado_por_dia: List[QuantidadeCertoErradoPorDia]