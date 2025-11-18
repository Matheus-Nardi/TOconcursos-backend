from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exists, and_
from models.questoes import questao as models
from schemas.questoes import questao as schemas
from schemas.questoes.filtro_questao import FiltroRequestDTO 
from models.questoes.comentario import Comentario
from models.usuarios.resolucao_questao import ResolucaoQuestao

class QuestaoRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_questao(self, questao: models.Questao) -> models.Questao:
        self.db.add(questao)
        self.db.commit()
        self.db.refresh(questao)
        return questao

    def get_questao_by_name(self, label: str) -> models.Questao:
        return (
            self.db.query(models.Questao)
            .options(
                joinedload(models.Questao.disciplina),
                joinedload(models.Questao.orgao),
                joinedload(models.Questao.banca),
                joinedload(models.Questao.instituicao)
            )
            .filter(models.Questao.label == label)
            .first()
        )
    
    def get_questao(self, questao_id: int) -> models.Questao:
        return (
            self.db.query(models.Questao)
            .options(
                joinedload(models.Questao.disciplina),
                joinedload(models.Questao.orgao),
                joinedload(models.Questao.banca),
                joinedload(models.Questao.instituicao),
                joinedload(models.Questao.alternativas)
            )
            .filter(models.Questao.id == questao_id)
            .first()
        )

    def get_all_questaos(self, skip: int = 0, limit: int = 10, usuario_id: int | None = None) -> list[models.Questao]:
        """
        Retorna todas as questões. Se usuario_id for fornecido, ordena as não respondidas primeiro.
        """
        query = (
            self.db.query(models.Questao)
            .options(
                joinedload(models.Questao.disciplina),
                joinedload(models.Questao.orgao),
                joinedload(models.Questao.banca),
                joinedload(models.Questao.instituicao)
            )
        )
        
        # Se usuario_id fornecido, ordena questões não respondidas primeiro
        if usuario_id:
            subquery = exists().where(
                and_(
                    ResolucaoQuestao.questao_id == models.Questao.id,
                    ResolucaoQuestao.usuario_id == usuario_id
                )
            )
            query = query.order_by(~subquery)  # ~ inverte: False (não respondidas) primeiro
        
        return query.offset(skip).limit(limit).all()
    
    def usuario_respondeu_questao(self, questao_id: int, usuario_id: int) -> bool:
        """
        Verifica se o usuário já respondeu a questão.
        """
        return (
            self.db.query(ResolucaoQuestao)
            .filter(
                and_(
                    ResolucaoQuestao.questao_id == questao_id,
                    ResolucaoQuestao.usuario_id == usuario_id
                )
            )
            .first() is not None
        )

    def get_all_comentarios(self, questao_id: int) -> list[Comentario]:
        return self.db.query(Comentario).filter(Comentario.id_questao == questao_id).all()

    def update_questao(self, questao_id: int, questao: schemas.QuestaoRequestDTO) -> models.Questao:
        db_questao = self.get_questao(questao_id)
        if db_questao:
            self.db.commit()
            self.db.refresh(db_questao)
        return db_questao


    def delete_questao(self, questao_id: int) -> bool:
        db_questao = self.get_questao(questao_id)
        if db_questao:
            self.db.delete(db_questao)
            self.db.commit()
            return True
        else:
            return False

    def filter_questao(self, filtro: FiltroRequestDTO, skip: int = 0, limit: int = 10, usuario_id: int | None = None) -> list[models.Questao]:
        query = self.db.query(models.Questao).options(
            joinedload(models.Questao.disciplina),
            joinedload(models.Questao.orgao),
            joinedload(models.Questao.banca),
            joinedload(models.Questao.instituicao)
        )

        # Filtro por ja_respondeu agora é específico do usuário
        if filtro.ja_respondeu is not None and usuario_id is not None:
            subquery = exists().where(
                and_(
                    ResolucaoQuestao.questao_id == models.Questao.id,
                    ResolucaoQuestao.usuario_id == usuario_id
                )
            )
            if filtro.ja_respondeu:
                query = query.filter(subquery)  # Apenas questões respondidas
            else:
                query = query.filter(~subquery)  # Apenas questões não respondidas
        
        if filtro.id_disciplina is not None:
            query = query.filter(models.Questao.id_disciplina == filtro.id_disciplina)
        if filtro.dificuldade is not None:
            query = query.filter(models.Questao.dificuldade == filtro.dificuldade)
        if filtro.id_banca is not None:
            query = query.filter(models.Questao.id_banca == filtro.id_banca)
        if filtro.id_orgao is not None:
            query = query.filter(models.Questao.id_orgao == filtro.id_orgao)
        if filtro.id_instituicao is not None:
            query = query.filter(models.Questao.id_instituicao == filtro.id_instituicao)
        if filtro.palavra_chave is not None:
            query = query.filter(models.Questao.enunciado.ilike(f"%{filtro.palavra_chave}%"))

        # Ordena questões não respondidas primeiro se usuario_id fornecido
        if usuario_id:
            subquery = exists().where(
                and_(
                    ResolucaoQuestao.questao_id == models.Questao.id,
                    ResolucaoQuestao.usuario_id == usuario_id
                )
            )
            query = query.order_by(~subquery)
        
        return query.offset(skip).limit(limit).all()