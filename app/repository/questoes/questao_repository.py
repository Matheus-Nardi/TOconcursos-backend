from sqlalchemy.orm import Session
from models.questoes import questao as models
from schemas.questoes import questao as schemas

class QuestaoRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_questao(self, questao: models.Questao) -> models.Questao:
        self.db.add(questao)
        self.db.commit()
        self.db.refresh(questao)
        return questao


    def get_questao_by_name(self, nome: str) -> models.Questao:
        return self.db.query(models.Questao).filter(models.Questao.nome == nome).first()
    
    def get_questao(self, questao_id: int) -> models.Questao:
        return self.db.get(models.Questao, questao_id)

    def get_all_questaos(self) -> list[models.Questao]:
        return self.db.query(models.Questao).all()
    
    def get_all_questaos(self, skip: int = 0, limit: int = 10) -> list[models.Questao]:
        return self.db.query(models.Questao).offset(skip).limit(limit).all()

    def update_questao(self, questao_id: int, questao: schemas.QuestaoRequestDTO) -> models.Questao:
        db_questao = self.get_questao(questao_id)
        if db_questao:
            db_questao.nome = questao.nome
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