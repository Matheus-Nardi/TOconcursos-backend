from sqlalchemy.orm import Session
from models.questoes import instituicao as models
from schemas.questoes import instituicao as schemas

class InstituicaoRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_instituicao(self, instituicao: schemas.InstituicaoRequestDTO) -> models.Instituicao:
        db_instituicao = models.Instituicao(nome=instituicao.nome)
        self.db.add(db_instituicao)
        self.db.commit()
        self.db.refresh(db_instituicao)
        return db_instituicao

    def get_instituicao_by_name(self, nome: str) -> models.Instituicao:
        return self.db.query(models.Instituicao).filter(models.Instituicao.nome == nome).first()
    
    def get_instituicao(self, instituicao_id: int) -> models.Instituicao:
        return self.db.get(models.Instituicao, instituicao_id)

    def get_all_instituicaos(self) -> list[models.Instituicao]:
        return self.db.query(models.Instituicao).all()
    
    def get_all_instituicaos(self, skip: int = 0, limit: int = 10) -> list[models.Instituicao]:
        return self.db.query(models.Instituicao).offset(skip).limit(limit).all()

    def update_instituicao(self, instituicao_id: int, instituicao: schemas.InstituicaoRequestDTO) -> models.Instituicao:
        db_instituicao = self.get_instituicao(instituicao_id)
        if db_instituicao:
            db_instituicao.nome = instituicao.nome
            self.db.commit()
            self.db.refresh(db_instituicao)
        return db_instituicao

    def delete_instituicao(self, instituicao_id: int) -> bool:
        db_instituicao = self.get_instituicao(instituicao_id)
        if db_instituicao:
            self.db.delete(db_instituicao)
            self.db.commit()
            return True
        else:
            return False