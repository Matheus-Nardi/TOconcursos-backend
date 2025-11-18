from pydantic import BaseModel
from typing import List
from .qtd_questao_por_dia import QuantidadeQuestoesPorDia
from .qtd_certo_errado_questao_por_dia import QuantidadeCertoErradoPorDia
from .percentual_acerto_por_disciplina import PercentualAcertoPorDisciplina
from .evolucao_percentual_acerto import EvolucaoPercentualAcerto
from .distribuicao_questoes_por_disciplina import DistribuicaoQuestoesPorDisciplina
from .percentual_acerto_por_orgao import PercentualAcertoPorOrgao
from .percentual_acerto_por_banca import PercentualAcertoPorBanca

class GraficosResponseDTO(BaseModel):
    quantidade_questoes_por_dia: List[QuantidadeQuestoesPorDia]
    quantidade_certo_errado_por_dia: List[QuantidadeCertoErradoPorDia]
    percentual_acerto_por_disciplina: List[PercentualAcertoPorDisciplina]
    evolucao_percentual_acerto: List[EvolucaoPercentualAcerto]
    distribuicao_questoes_por_disciplina: List[DistribuicaoQuestoesPorDisciplina]
    percentual_acerto_por_orgao: List[PercentualAcertoPorOrgao]
    percentual_acerto_por_banca: List[PercentualAcertoPorBanca]