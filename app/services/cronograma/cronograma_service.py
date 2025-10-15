
from schemas.cronograma import cronograma as schemas
from sqlalchemy.orm import Session
from models.cronograma.cronograma import Cronograma
from repository.cronograma.cronograma_repository import CronogramaRepository
from repository.questoes.disciplina_repository import DisciplinaRepository
from datetime import datetime
from models.cronograma import estudo_diario as models
from repository.usuarios.usuario_repository import UsuarioRepository

class CronogramaService:
    def __init__(self, db: Session):
        self.repo = CronogramaRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    def create_cronograma(self, user_id: int, cronograma: schemas.CronogramaRequestDTO) -> schemas.CronogramaResponseDTO:

        for estudo in cronograma.estudos_diarios:
            if estudo.hora_fim <= estudo.hora_inicio:
                raise ValueError("hora_fim deve ser maior que hora_inicio")
            
        db_user = self.usuario_repo.get_usuario(user_id)
        if not db_user:
            raise ValueError("Usuário não encontrado")
        
        db_estudos_diarios = [
            models.EstudoDiario(
                hora_inicio=estudo.hora_inicio,
                hora_fim=estudo.hora_fim,
                dia_da_semana=estudo.dia_da_semana,
                disciplina=self.disciplina_repo.get_by_id(estudo.id_disciplina)
            )
            for estudo in cronograma.estudos_diarios
        ]
        db_cronograma = Cronograma(
            nome=cronograma.nome,
            descricao=cronograma.descricao,
            data_criacao=datetime.now(),
            estudos_diarios=db_estudos_diarios,
            usuario=db_user
        )

        db_cronograma = self.repo.create_cronograma(db_cronograma)
        return schemas.CronogramaResponseDTO.model_validate(db_cronograma)

    def get_cronograma(self, user_id:int, cronograma_id: int) -> schemas.CronogramaResponseDTO:
        db_cronograma = self.repo.get_cronograma(cronograma_id, user_id)
        if db_cronograma:
            return schemas.CronogramaResponseDTO.model_validate(db_cronograma)
        return None

    def get_all_cronogramas(self, user_id:int, skip, limit) -> list[schemas.CronogramaResponseDTO]:
        cronogramas = self.repo.get_all_cronogramas(user_id=user_id, skip=skip, limit=limit)
        return [schemas.CronogramaResponseDTO.model_validate(d) for d in cronogramas]

    def delete_cronograma(self, user_id:int, cronograma_id: int) -> bool:
        db_cronograma = self.repo.get_cronograma(cronograma_id, user_id)
        if not db_cronograma:
            raise ValueError("Cronograma não encontrado")
        return self.repo.delete_cronograma(cronograma_id, user_id)
    

    # def filter_cronograma(self, filtro: FiltroRequestDTO, skip: int = 0, limit: int = 10) -> list[schemas.CronogramaResponseDTO]:
    #     cronograma = self.repo.filter_cronograma(filtro=filtro, skip=skip, limit=limit)
    #     return [schemas.CronogramaResponseDTO.model_validate(d) for d in cronograma]
