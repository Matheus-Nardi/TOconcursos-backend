from sqlalchemy.orm import Session
from models.questoes import disciplina as models
from schemas.questoes import disciplina as schemas

class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_disciplina(self, disciplina: schemas.DisciplinaRequestDTO) -> models.Disciplina:
        db_disciplina = models.Disciplina(nome=disciplina.nome)
        self.db.add(db_disciplina)
        self.db.commit()
        self.db.refresh(db_disciplina)
        return db_disciplina

    def get_disciplina_by_name(self, nome: str) -> models.Disciplina:
        return self.db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()
    
    def get_disciplina(self, disciplina_id: int) -> models.Disciplina:
        return self.db.get(models.Disciplina, disciplina_id)

    def get_all_disciplinas(self) -> list[models.Disciplina]:
        return self.db.query(models.Disciplina).all()

    def update_disciplina(self, disciplina_id: int, disciplina: schemas.DisciplinaRequestDTO) -> models.Disciplina:
        db_disciplina = self.get_disciplina(disciplina_id)
        if db_disciplina:
            db_disciplina.nome = disciplina.nome
            self.db.commit()
            self.db.refresh(db_disciplina)
        return db_disciplina

    def delete_disciplina(self, disciplina_id: int) -> bool:
        db_disciplina = self.get_disciplina(disciplina_id)
        if db_disciplina:
            self.db.delete(db_disciplina)
            self.db.commit()
            return True
        else:
            return False