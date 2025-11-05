from sqlalchemy.orm import Session
from models.usuarios.objetivo import Objetivo

class ObjetivoRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_all_objetivos(self, skip: int = 0, limit: int = 10) -> list[Objetivo]:
        return self.db.query(Objetivo).offset(skip).limit(limit).all()
    
    def get_objetivo(self, objetivo_id: int) -> Objetivo | None:
        return self.db.query(Objetivo).filter(Objetivo.id == objetivo_id).first()