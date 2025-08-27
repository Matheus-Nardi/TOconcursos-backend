from sqlalchemy.orm import Session
from models.questoes import banca as models

class BancaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, banca: models.Banca) -> models.Banca:
        """
        Salva uma instância da banca (serve tanto para criar quanto para atualizar).
        O SQLAlchemy rastreia as mudanças no objeto.
        """
        self.db.add(banca)
        self.db.commit()
        self.db.refresh(banca)
        return banca

    def get_by_id(self, banca_id: int) -> models.Banca | None:
        """ Busca uma banca pelo seu ID. """
        return self.db.get(models.Banca, banca_id)

    def get_by_name(self, label: str) -> models.Banca | None:
        """ Busca uma banca pelo label. """
        return self.db.query(models.Banca).filter(models.Banca.label == label).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Banca]:
        """
        Retorna uma lista de bancas com paginação.
        (Corrigido: unificando os dois métodos 'get_all_bancas' em um só).
        """
        return self.db.query(models.Banca).offset(skip).limit(limit).all()

    def delete(self, banca: models.Banca) -> None:
        """ Deleta uma instância da banca. """
        self.db.delete(banca)
        self.db.commit()