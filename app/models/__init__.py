# Import all models for Alembic to recognize them
from .cronograma.cronograma import Cronograma
from .cronograma.estudo_diario import EstudoDiario
from .pagamento.pagamento import Pagamento
from .pagamento.boleto import Boleto
from .pagamento.pix import Pix
from .planos.plano import Plano
from .pagamento.cartao import Cartao
from .questoes.alternativa import Alternativa
from .questoes.banca import Banca
from .questoes.comentario import Comentario
from .questoes.disciplina import Disciplina
from .questoes.instituicao import Instituicao
from .questoes.orgao import Orgao
from .questoes.questao import Questao
from .usuarios.usuario import Usuario
from .usuarios.resolucao_questao import ResolucaoQuestao
