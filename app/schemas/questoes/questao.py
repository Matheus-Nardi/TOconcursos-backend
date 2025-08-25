from models.questoes.dificuldade import DificuldadeEnum
from pydantic import BaseModel
from schemas.questoes.alternativa import AlternativaRequestDTO, AlternativaResponseDTO
from schemas.questoes.disciplina import DisciplinaResponseDTO


from schemas.questoes.orgao import OrgaoResponseDTO
from schemas.questoes.instituicao import InstituicaoResponseDTO
from schemas.questoes.banca import BancaResponseDTO


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
    dificuldade: DificuldadeEnum
    disciplina: DisciplinaResponseDTO
    orgao: OrgaoResponseDTO
    instituicao: InstituicaoResponseDTO
    banca: BancaResponseDTO
    alternativas: list[AlternativaResponseDTO]

    model_config = {
        "from_attributes": True
    }
        
        
        