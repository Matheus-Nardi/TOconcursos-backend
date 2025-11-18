from sqlalchemy.orm import Session
from repository.usuarios.resolucao_questao_repository import ResolucaoQuestaoRepository

class GraficosService:
    def __init__(self, db: Session):
        self.repo = ResolucaoQuestaoRepository(db)

    def get_quantidade_questoes_por_dia(self, usuario_id: int):
        return self.repo.get_quantidade_questoes_por_dia(usuario_id)

    def get_quantidade_certo_errado_por_dia(self, usuario_id: int):
        return self.repo.get_quantidade_certo_errado_por_dia(usuario_id)

    def get_percentual_acerto_por_disciplina(self, usuario_id: int):
        return self.repo.get_percentual_acerto_por_disciplina(usuario_id)

    def get_evolucao_percentual_acerto(self, usuario_id: int):
        return self.repo.get_evolucao_percentual_acerto(usuario_id)

    def get_distribuicao_questoes_por_disciplina(self, usuario_id: int):
        return self.repo.get_distribuicao_questoes_por_disciplina(usuario_id)

    def get_percentual_acerto_por_orgao(self, usuario_id: int):
        return self.repo.get_percentual_acerto_por_orgao(usuario_id)

    def get_percentual_acerto_por_banca(self, usuario_id: int):
        return self.repo.get_percentual_acerto_por_banca(usuario_id)
