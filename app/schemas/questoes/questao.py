from models.questoes.dificuldade import DificuldadeEnum
from pydantic import BaseModel
from typing import Optional
from schemas.questoes.alternativa import AlternativaRequestDTO, AlternativaResponseDTO
from schemas.questoes.disciplina import DisciplinaResponseDTO


from schemas.questoes.orgao import OrgaoResponseDTO
from schemas.questoes.instituicao import InstituicaoResponseDTO
from schemas.questoes.banca import BancaResponseDTO
from schemas.questoes.comentario import ComentarioResponseDTO

class QuestaoRequestDTO(BaseModel):
    enunciado: str
    id_disciplina: int
    dificuldade: DificuldadeEnum = DificuldadeEnum.FACIL
    id_orgao: int
    id_instituicao: int
    id_banca: int
    alternativas: list[AlternativaRequestDTO]

class QuestaoResponseDTO(BaseModel):
    id: int
    enunciado: str
    enunciado_linhas: list[str] | None = None
    dificuldade: DificuldadeEnum
    disciplina: Optional[DisciplinaResponseDTO] = None
    orgao: Optional[OrgaoResponseDTO] = None
    instituicao: Optional[InstituicaoResponseDTO] = None
    banca: Optional[BancaResponseDTO] = None
    alternativas: list[AlternativaResponseDTO]
    ja_respondeu: Optional[bool] = False  # Calculado dinamicamente baseado no usuário
    comentarios: list[ComentarioResponseDTO] = []

    model_config = {
        "from_attributes": True
    }

class QuestaoSimplificadaResponseDTO(BaseModel):
    id: int
    enunciado: str
    ja_respondeu: bool

    model_config = {
        "from_attributes": True
    }
        
        
        