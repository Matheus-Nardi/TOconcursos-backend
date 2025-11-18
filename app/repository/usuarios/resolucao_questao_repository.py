from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from models.usuarios.resolucao_questao import ResolucaoQuestao
from models.questoes.questao import Questao
from models.questoes.disciplina import Disciplina
from models.questoes.orgao import Orgao
from models.questoes.banca import Banca
from schemas.estatisticas.graficos.qtd_questao_por_dia import QuantidadeQuestoesPorDia
from schemas.estatisticas.graficos.qtd_certo_errado_questao_por_dia import QuantidadeCertoErradoPorDia
from schemas.estatisticas.graficos.percentual_acerto_por_disciplina import PercentualAcertoPorDisciplina
from schemas.estatisticas.graficos.evolucao_percentual_acerto import EvolucaoPercentualAcerto
from schemas.estatisticas.graficos.distribuicao_questoes_por_disciplina import DistribuicaoQuestoesPorDisciplina
from schemas.estatisticas.graficos.percentual_acerto_por_orgao import PercentualAcertoPorOrgao
from schemas.estatisticas.graficos.percentual_acerto_por_banca import PercentualAcertoPorBanca

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

    def get_percentual_acerto_por_disciplina(self, usuario_id: int) -> list[PercentualAcertoPorDisciplina]:
        """
        Retorna o percentual de acerto por disciplina para um usuário específico.
        """
        resultado = (
            self.db.query(
                Disciplina.id.label('disciplina_id'),
                Disciplina.label.label('disciplina_nome'),
                func.count(ResolucaoQuestao.id).label('total_questoes'),
                func.sum(case((ResolucaoQuestao.is_certa == True, 1), else_=0)).label('total_acertos'),
                func.sum(case((ResolucaoQuestao.is_certa == False, 1), else_=0)).label('total_erros')
            )
            .join(Questao, ResolucaoQuestao.questao_id == Questao.id)
            .join(Disciplina, Questao.id_disciplina == Disciplina.id)
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .group_by(Disciplina.id, Disciplina.label)
            .order_by(func.count(ResolucaoQuestao.id).desc())
            .all()
        )
        
        return [
            PercentualAcertoPorDisciplina(
                disciplina_id=row.disciplina_id,
                disciplina_nome=row.disciplina_nome,
                total_questoes=int(row.total_questoes or 0),
                total_acertos=int(row.total_acertos or 0),
                total_erros=int(row.total_erros or 0),
                percentual_acerto=round((int(row.total_acertos or 0) / int(row.total_questoes or 1)) * 100, 2)
            )
            for row in resultado
        ]

    

    def get_evolucao_percentual_acerto(self, usuario_id: int) -> list[EvolucaoPercentualAcerto]:
        """
        Retorna a evolução do percentual de acerto ao longo do tempo (por dia).
        """
        resultado = (
            self.db.query(
                func.date(ResolucaoQuestao.data_resolucao).label('data'),
                func.count(ResolucaoQuestao.id).label('total_questoes'),
                func.sum(case((ResolucaoQuestao.is_certa == True, 1), else_=0)).label('total_acertos')
            )
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .group_by(func.date(ResolucaoQuestao.data_resolucao))
            .order_by(func.date(ResolucaoQuestao.data_resolucao))
            .all()
        )
        
        return [
            EvolucaoPercentualAcerto(
                data=row.data,
                total_questoes=int(row.total_questoes or 0),
                percentual_acerto=round((int(row.total_acertos or 0) / int(row.total_questoes or 1)) * 100, 2)
            )
            for row in resultado
        ]

    def get_distribuicao_questoes_por_disciplina(self, usuario_id: int) -> list[DistribuicaoQuestoesPorDisciplina]:
        """
        Retorna a distribuição (quantidade e percentual) de questões resolvidas por disciplina.
        """
        # Primeiro, calcular o total de questões
        total_questoes = (
            self.db.query(func.count(ResolucaoQuestao.id))
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .scalar() or 0
        )
        
        if total_questoes == 0:
            return []
        
        resultado = (
            self.db.query(
                Disciplina.id.label('disciplina_id'),
                Disciplina.label.label('disciplina_nome'),
                func.count(ResolucaoQuestao.id).label('quantidade_questoes')
            )
            .join(Questao, ResolucaoQuestao.questao_id == Questao.id)
            .join(Disciplina, Questao.id_disciplina == Disciplina.id)
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .group_by(Disciplina.id, Disciplina.label)
            .order_by(func.count(ResolucaoQuestao.id).desc())
            .all()
        )
        
        return [
            DistribuicaoQuestoesPorDisciplina(
                disciplina_id=row.disciplina_id,
                disciplina_nome=row.disciplina_nome,
                quantidade_questoes=int(row.quantidade_questoes or 0),
                percentual_total=round((int(row.quantidade_questoes or 0) / total_questoes) * 100, 2)
            )
            for row in resultado
        ]

    def get_percentual_acerto_por_orgao(self, usuario_id: int) -> list[PercentualAcertoPorOrgao]:
        """
        Retorna o percentual de acerto por órgão para um usuário específico.
        """
        resultado = (
            self.db.query(
                Orgao.id.label('orgao_id'),
                Orgao.label.label('orgao_nome'),
                func.count(ResolucaoQuestao.id).label('total_questoes'),
                func.sum(case((ResolucaoQuestao.is_certa == True, 1), else_=0)).label('total_acertos'),
                func.sum(case((ResolucaoQuestao.is_certa == False, 1), else_=0)).label('total_erros')
            )
            .join(Questao, ResolucaoQuestao.questao_id == Questao.id)
            .join(Orgao, Questao.id_orgao == Orgao.id)
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .group_by(Orgao.id, Orgao.label)
            .order_by(func.count(ResolucaoQuestao.id).desc())
            .all()
        )
        
        return [
            PercentualAcertoPorOrgao(
                orgao_id=row.orgao_id,
                orgao_nome=row.orgao_nome,
                total_questoes=int(row.total_questoes or 0),
                total_acertos=int(row.total_acertos or 0),
                total_erros=int(row.total_erros or 0),
                percentual_acerto=round((int(row.total_acertos or 0) / int(row.total_questoes or 1)) * 100, 2)
            )
            for row in resultado
        ]

    def get_percentual_acerto_por_banca(self, usuario_id: int) -> list[PercentualAcertoPorBanca]:
        """
        Retorna o percentual de acerto por banca para um usuário específico.
        """
        resultado = (
            self.db.query(
                Banca.id.label('banca_id'),
                Banca.label.label('banca_nome'),
                func.count(ResolucaoQuestao.id).label('total_questoes'),
                func.sum(case((ResolucaoQuestao.is_certa == True, 1), else_=0)).label('total_acertos'),
                func.sum(case((ResolucaoQuestao.is_certa == False, 1), else_=0)).label('total_erros')
            )
            .join(Questao, ResolucaoQuestao.questao_id == Questao.id)
            .join(Banca, Questao.id_banca == Banca.id)
            .filter(ResolucaoQuestao.usuario_id == usuario_id)
            .group_by(Banca.id, Banca.label)
            .order_by(func.count(ResolucaoQuestao.id).desc())
            .all()
        )
        
        return [
            PercentualAcertoPorBanca(
                banca_id=row.banca_id,
                banca_nome=row.banca_nome,
                total_questoes=int(row.total_questoes or 0),
                total_acertos=int(row.total_acertos or 0),
                total_erros=int(row.total_erros or 0),
                percentual_acerto=round((int(row.total_acertos or 0) / int(row.total_questoes or 1)) * 100, 2)
            )
            for row in resultado
        ]


    
