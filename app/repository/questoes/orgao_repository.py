from sqlalchemy.orm import Session
from models.questoes import orgao as models
from schemas.questoes import orgao as schemas

class OrgaoRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_orgao(self, orgao: schemas.OrgaoRequestDTO) -> models.Orgao:
        db_orgao = models.Orgao(nome=orgao.nome)
        self.db.add(db_orgao)
        self.db.commit()
        self.db.refresh(db_orgao)
        return db_orgao

    def get_orgao_by_name(self, nome: str) -> models.Orgao:
        return self.db.query(models.Orgao).filter(models.Orgao.nome == nome).first()
    
    def get_orgao(self, orgao_id: int) -> models.Orgao:
        return self.db.get(models.Orgao, orgao_id)

    def get_all_orgaos(self) -> list[models.Orgao]:
        return self.db.query(models.Orgao).all()
    
    def get_all_orgaos(self, skip: int = 0, limit: int = 10) -> list[models.Orgao]:
        return self.db.query(models.Orgao).offset(skip).limit(limit).all()

    def update_orgao(self, orgao_id: int, orgao: schemas.OrgaoRequestDTO) -> models.Orgao:
        db_orgao = self.get_orgao(orgao_id)
        if db_orgao:
            db_orgao.nome = orgao.nome
            self.db.commit()
            self.db.refresh(db_orgao)
        return db_orgao

    def delete_orgao(self, orgao_id: int) -> bool:
        db_orgao = self.get_orgao(orgao_id)
        if db_orgao:
            self.db.delete(db_orgao)
            self.db.commit()
            return True
        else:
            return False