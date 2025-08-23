from sqlalchemy.orm import Session
from models.questoes import banca as models
from schemas.questoes import banca as schemas

class BancaRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_banca(self, banca: schemas.BancaRequestDTO) -> models.Banca:
        db_banca = models.Banca(nome=banca.nome)
        self.db.add(db_banca)
        self.db.commit()
        self.db.refresh(db_banca)
        return db_banca

    def get_banca_by_name(self, nome: str) -> models.Banca:
        return self.db.query(models.Banca).filter(models.Banca.nome == nome).first()
    
    def get_banca(self, banca_id: int) -> models.Banca:
        return self.db.get(models.Banca, banca_id)

    def get_all_bancas(self) -> list[models.Banca]:
        return self.db.query(models.Banca).all()
    
    def get_all_bancas(self, skip: int = 0, limit: int = 10) -> list[models.Banca]:
        return self.db.query(models.Banca).offset(skip).limit(limit).all()

    def update_banca(self, banca_id: int, banca: schemas.BancaRequestDTO) -> models.Banca:
        db_banca = self.get_banca(banca_id)
        if db_banca:
            db_banca.nome = banca.nome
            self.db.commit()
            self.db.refresh(db_banca)
        return db_banca

    def delete_banca(self, banca_id: int) -> bool:
        db_banca = self.get_banca(banca_id)
        if db_banca:
            self.db.delete(db_banca)
            self.db.commit()
            return True
        else:
            return False