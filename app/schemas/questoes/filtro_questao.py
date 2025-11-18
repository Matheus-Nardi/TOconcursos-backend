from pydantic import BaseModel
from models.questoes import DificuldadeEnum
from typing import List
from schemas.questoes.disciplina import DisciplinaResponseDTO
from schemas.questoes.orgao import OrgaoResponseDTO
from schemas.questoes.instituicao import InstituicaoResponseDTO
from schemas.questoes.banca import BancaResponseDTO
class FiltroRequestDTO(BaseModel):
    ja_respondeu: bool | None = None
    id_disciplina: int | None = None
    dificuldade: DificuldadeEnum | None = None
    id_banca: int | None = None
    id_orgao: int | None = None
    id_instituicao: int | None = None
    palavra_chave: str | None = None

class FiltroResponseDTO(BaseModel):
    disciplinas: List[DisciplinaResponseDTO]
    orgaos: List[OrgaoResponseDTO]
    instituicoes: List[InstituicaoResponseDTO]
    bancas: List[BancaResponseDTO]