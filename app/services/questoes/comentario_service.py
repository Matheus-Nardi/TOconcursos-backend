from schemas.questoes import comentario as schemas
from sqlalchemy.orm import Session
from models.questoes.comentario import Comentario
from repository.questoes.comentario_repository import ComentarioRepository
from repository.usuarios.usuario_repository import UsuarioRepository
from repository.questoes.questao_repository import QuestaoRepository
from fastapi import HTTPException
from schemas.usuarios.usuario import UsuarioResponseDTO
from starlette import status

class ComentarioService:
    def __init__(self, db: Session):
        self.repo = ComentarioRepository(db)
        self.user_repo = UsuarioRepository(db)
        self.questao_repo = QuestaoRepository(db)

    def create_comentario(self, comentario_dto: schemas.ComentarioRequestDTO, current_user: UsuarioResponseDTO) -> schemas.ComentarioResponseDTO:
        user_db, questao_db = self.get_user_and_question(comentario_dto, current_user)

        db_comentario = Comentario(
            comentario=comentario_dto.comentario,
            data_comentario=comentario_dto.data_comentario,
            questao=questao_db,
            usuario=user_db
        )
        saved_comentario = self.repo.save(db_comentario)
        
        return schemas.ComentarioResponseDTO.model_validate(saved_comentario)

    def get_user_and_question(self, comentario_dto, current_user):
        user_db = self.user_repo.get_usuario(current_user.id)
        if not user_db:
            raise ValueError(f"Usuário com id {current_user.id} não encontrado.")

        questao_db = self.questao_repo.get_questao(comentario_dto.id_questao)
        if not questao_db:
                raise ValueError(f"Questão com id {comentario_dto.id_questao} não encontrada.")
        return user_db,questao_db

    def get_comentario(self, comentario_id: int) -> schemas.ComentarioResponseDTO:
        db_comentario = self.repo.get_by_id(comentario_id)
        
        if not db_comentario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Comentario não encontrada."
            )
            
        return schemas.ComentarioResponseDTO.model_validate(db_comentario)

    def get_all_comentarios(self, skip: int = 0, limit: int = 100) -> list[schemas.ComentarioResponseDTO]:
        comentarios = self.repo.get_all(skip=skip, limit=limit)
        return [schemas.ComentarioResponseDTO.model_validate(b) for b in comentarios]
    
    def get_comentarios_by_questao(self, questao_id: int, skip: int = 0, limit: int = 100) -> list[schemas.ComentarioResponseDTO]:
        comentarios = self.repo.get_comentarios_by_questao(questao_id, skip=skip, limit=limit)
        return [schemas.ComentarioResponseDTO.model_validate(b) for b in comentarios]

    def update_comentario(self, comentario_id: int, comentario_dto: schemas.ComentarioRequestDTO, current_user: UsuarioResponseDTO) -> schemas.ComentarioResponseDTO:
        user_db, questao_db = self.get_user_and_question(comentario_dto, current_user)
        if not user_db and user_db.id != current_user.id:
            raise ValueError(f"Usuário com id {current_user.id} não encontrado.")
        
        db_comentario = self.repo.get_by_id(comentario_id)
        if not db_comentario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Comentario não encontrada para atualização."
            )
        
        db_comentario.comentario = comentario_dto.comentario
        db_comentario.data_comentario = comentario_dto.data_comentario
        db_comentario.questao = questao_db
        db_comentario.usuario = user_db
    
        updated_comentario = self.repo.save(db_comentario)  
    
        return schemas.ComentarioResponseDTO.model_validate(updated_comentario)

    def delete_comentario(self, comentario_id: int, current_user: UsuarioResponseDTO) -> None:
        db_user = self.user_repo.get_usuario(current_user.id)
        if not db_user and db_user.id != current_user.id:
            raise ValueError(f"Usuário com id {current_user.id} não encontrado.")
        
        db_comentario = self.repo.get_by_id(comentario_id)
        if not db_comentario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario não encontrada para exclusão."
            )
        
        self.repo.delete(db_comentario)
        
        return
