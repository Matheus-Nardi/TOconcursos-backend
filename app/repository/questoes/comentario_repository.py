from sqlalchemy.orm import Session
from models.questoes import comentario as models

class ComentarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, comentario: models.Comentario) -> models.Comentario:
        """
        Salva uma instância da comentario (serve tanto para criar quanto para atualizar).
        O SQLAlchemy rastreia as mudanças no objeto.
        """
        self.db.add(comentario)
        self.db.commit()
        self.db.refresh(comentario)
        return comentario

    def get_by_id(self, comentario_id: int) -> models.Comentario | None:
        """ Busca uma comentario pelo seu ID. """
        return self.db.get(models.Comentario, comentario_id)

    def get_by_user(self, usuario_id: int) -> list[models.Comentario]:
        """ Busca comentarios pelo ID do usuário. """
        return self.db.query(models.Comentario).filter(models.Comentario.id_usuario == usuario_id).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[models.Comentario]:
        """
        Retorna uma lista de comentarios com paginação.
        (Corrigido: unificando os dois métodos 'get_all_comentarios' em um só).
        """
        return self.db.query(models.Comentario).offset(skip).limit(limit).all()
    
    def get_comentarios_by_questao(self, questao_id: int, skip: int = 0, limit: int = 100) -> list[models.Comentario]:
        """ Busca comentarios pelo ID da questão com paginação. """
        return self.db.query(models.Comentario).filter(models.Comentario.id_questao == questao_id).offset(skip).limit(limit).all()

    def delete(self, comentario: models.Comentario) -> None:
        """ Deleta uma instância da comentario. """
        self.db.delete(comentario)
        self.db.commit()
