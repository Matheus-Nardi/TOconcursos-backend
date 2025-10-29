from sqlalchemy.orm import Session
from models.planos import plano as models

class PlanoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_plano: int) -> models.Plano | None:
        return self.db.get(models.Plano, id_plano)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Plano]:
        return self.db.query(models.Plano).offset(skip).limit(limit).all()
