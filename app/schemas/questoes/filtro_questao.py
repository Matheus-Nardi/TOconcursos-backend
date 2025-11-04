from pydantic import BaseModel
from models.questoes import DificuldadeEnum

class FiltroRequestDTO(BaseModel):
    ja_respondeu: bool | None = None
    id_disciplina: int | None = None
    dificuldade: DificuldadeEnum | None = None
    id_banca: int | None = None
    id_orgao: int | None = None
    id_instituicao: int | None = None
