from .disciplina_router import router as disciplina_router
from .orgao_router import router as orgao_router
from .instituicao_router import router as instituicao_router
from .banca_router import router as banca_router
from .questao_router import router as questao_router
from .auth_router import router as auth_router
from .usuario_router import router as usuario_router
from .cronograma_router import router as cronograma_router
from .resolucao_questao_router import router as resolucao_questao_router
from .comentario_router import router as comentario_router
from .plano_router import router as plano_router

all_routers = [
    disciplina_router,
    orgao_router,
    instituicao_router,
    banca_router,
    questao_router,
    auth_router,
    usuario_router,
    cronograma_router,
    resolucao_questao_router,
    comentario_router,
    plano_router,
]