from sqlalchemy.orm import Session
from models.questoes import disciplina as models

class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, disciplina: models.Disciplina) -> models.Disciplina:
        """
        Salva uma instância de Disciplina (cria ou atualiza).
        """
        self.db.add(disciplina)
        self.db.commit()
        self.db.refresh(disciplina)
        return disciplina

    def get_by_id(self, disciplina_id: int) -> models.Disciplina | None:
        """ Busca uma disciplina pelo seu ID. """
        return self.db.get(models.Disciplina, disciplina_id)

    def get_by_name(self, nome: str) -> models.Disciplina | None:
        """ Busca uma disciplina pelo nome. """
        return self.db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Disciplina]:
        """ Retorna uma lista de disciplinas com paginação. """
        return self.db.query(models.Disciplina).offset(skip).limit(limit).all()

    def delete(self, disciplina: models.Disciplina) -> None:
        """ Deleta uma instância de Disciplina. """
        self.db.delete(disciplina)
        self.db.commit()