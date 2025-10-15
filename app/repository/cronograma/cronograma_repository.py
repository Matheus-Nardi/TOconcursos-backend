from sqlalchemy.orm import Session
from models.cronograma import cronograma as models
from schemas.cronograma import cronograma as schemas


class CronogramaRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_cronograma(self, cronograma: models.Cronograma) -> models.Cronograma:
        self.db.add(cronograma)
        self.db.commit()
        self.db.refresh(cronograma)
        return cronograma
        
    def get_cronograma(self, cronograma_id: int, user_id: int) -> models.Cronograma:
        return self.db.query(models.Cronograma).filter(models.Cronograma.id == cronograma_id, models.Cronograma.usuario_id == user_id).first()

    def get_all_cronogramas(self) -> list[models.Cronograma]:
        return self.db.query(models.Cronograma).all()

    def get_all_cronogramas(self, user_id: int, skip: int = 0, limit: int = 10) -> list[models.Cronograma]:
        return self.db.query(models.Cronograma).filter(models.Cronograma.usuario_id == user_id).offset(skip).limit(limit).all()

    def update_cronograma(self, cronograma_id: int, cronograma: schemas.CronogramaRequestDTO, user_id: int) -> models.Cronograma:
        db_cronograma = self.get_cronograma(cronograma_id)
        if db_cronograma and db_cronograma.usuario_id == user_id:
            self.db.commit()
            self.db.refresh(db_cronograma)
        return db_cronograma

    def delete_cronograma(self, cronograma_id: int, user_id: int) -> bool:
        db_cronograma = self.get_cronograma(cronograma_id, user_id=user_id)
        if db_cronograma and db_cronograma.usuario_id == user_id:
            self.db.delete(db_cronograma)
            self.db.commit()
            return True
        else:
            return False

    # def filter_cronograma(self, filtro: FiltroRequestDTO, skip: int = 0, limit: int = 10) -> list[models.Cronograma]:
    #     query = self.db.query(models.Cronograma)

    #     if filtro.ja_respondeu is not None:
    #         query = query.filter(models.Cronograma.ja_respondeu == filtro.ja_respondeu)
    #     if filtro.id_disciplina is not None:
    #         query = query.filter(models.Cronograma.id_disciplina == filtro.id_disciplina)
    #     if filtro.dificuldade is not None:
    #         query = query.filter(models.Cronograma.dificuldade == filtro.dificuldade)
    #     if filtro.id_banca is not None:
    #         query = query.filter(models.Cronograma.id_banca == filtro.id_banca)
    #     if filtro.id_orgao is not None:
    #         query = query.filter(models.Cronograma.id_orgao == filtro.id_orgao)
    #     if filtro.id_instituicao is not None:
    #         query = query.filter(models.Cronograma.id_instituicao == filtro.id_instituicao)

    #     return query.offset(skip).limit(limit).all()