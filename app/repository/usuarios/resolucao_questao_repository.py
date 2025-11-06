from sqlalchemy.orm import Session
from sqlalchemy import func, Date, case
from models.usuarios.resolucao_questao import ResolucaoQuestao
from schemas.estatisticas.graficos.qtd_questao_por_dia import QuantidadeQuestoesPorDia
from schemas.estatisticas.graficos.qtd_certo_errado_questao_por_dia import QuantidadeCertoErradoPorDia

class ResolucaoQuestaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_resolucao(self, resolucao: ResolucaoQuestao) -> ResolucaoQuestao:
        self.db.add(resolucao)
        self.db.commit()
        self.db.refresh(resolucao)
        return resolucao


    def get_all_resolucoes(self, skip: int = 0, limit: int = 10, user_id: int = 0) -> list[ResolucaoQuestao]:
        return self.db.query(ResolucaoQuestao).filter(ResolucaoQuestao.usuario_id == user_id).offset(skip).limit(limit).all()

    def get_quantidade_questoes_por_dia(self, user_id: int) -> list[QuantidadeQuestoesPorDia]:
        """
        Retorna a quantidade de questões resolvidas por dia para um usuário específico.
        Série histórica completa ordenada por data.
        """
        resultado = (
            self.db.query(
                func.date(ResolucaoQuestao.data_resolucao).label('data'),
                func.count(ResolucaoQuestao.id).label('quantidade_questoes')
            )
            .filter(ResolucaoQuestao.usuario_id == user_id)
            .group_by(func.date(ResolucaoQuestao.data_resolucao))
            .order_by(func.date(ResolucaoQuestao.data_resolucao))
            .all()
        )
        
        return [
            QuantidadeQuestoesPorDia(
                data=row.data,
                quantidade_questoes=row.quantidade_questoes
            )
            for row in resultado
        ]

    def get_quantidade_certo_errado_por_dia(self, user_id: int) -> list[QuantidadeCertoErradoPorDia]:
        """
        Retorna a quantidade de questões certas e erradas por dia para um usuário específico.
        Série histórica completa ordenada por data.
        """
        resultado = (
            self.db.query(
                func.date(ResolucaoQuestao.data_resolucao).label('data'),
                func.sum(case((ResolucaoQuestao.is_certa == True, 1), else_=0)).label('quantidade_questoes_certas'),
                func.sum(case((ResolucaoQuestao.is_certa == False, 1), else_=0)).label('quantidade_questoes_erradas')
            )
            .filter(ResolucaoQuestao.usuario_id == user_id)
            .group_by(func.date(ResolucaoQuestao.data_resolucao))
            .order_by(func.date(ResolucaoQuestao.data_resolucao))
            .all()
        )
        
        return [
            QuantidadeCertoErradoPorDia(
                data=row.data,
                quantidade_questoes_certas=int(row.quantidade_questoes_certas or 0),
                quantidade_questoes_erradas=int(row.quantidade_questoes_erradas or 0)
            )
            for row in resultado
        ]
    

    
