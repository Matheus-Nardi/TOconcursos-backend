from sqlalchemy.orm import Session
from models.questoes import instituicao as models

class InstituicaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, instituicao: models.Instituicao) -> models.Instituicao:
        """
        Salva uma instância de Instituicao (cria ou atualiza).
        """
        self.db.add(instituicao)
        self.db.commit()
        self.db.refresh(instituicao)
        return instituicao

    def get_by_id(self, instituicao_id: int) -> models.Instituicao | None:
        """ Busca uma instituição pelo seu ID. """
        return self.db.get(models.Instituicao, instituicao_id)

    def get_by_name(self, nome: str) -> models.Instituicao | None:
        """ Busca uma instituição pelo nome. """
        return self.db.query(models.Instituicao).filter(models.Instituicao.nome == nome).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Instituicao]:
        """ 
        Retorna uma lista de instituições com paginação.
        (Corrigido: unificando os dois métodos 'get_all_instituicaos').
        """
        return self.db.query(models.Instituicao).offset(skip).limit(limit).all()

    def delete(self, instituicao: models.Instituicao) -> None:
        """ Deleta uma instância de Instituicao. """
        self.db.delete(instituicao)
        self.db.commit()