from schemas.questoes.alternativa import AlternativaResponseDTO
from schemas.questoes.comentario import ComentarioResponseDTO
from pydantic import BaseModel
from typing import List, Optional

class QuestaoRequestDTO(BaseModel):
    enunciado: str
    instituicao_id: int
    dificuldade_id: int
    banca_id: int

class QuestaoResponseDTO(BaseModel):
    id: int
    enunciado: str
    instituicao_id: int
    dificuldade_id: int
    banca_id: int
    alternativas: Optional[List[AlternativaResponseDTO]] = None
    comentarios: Optional[List[ComentarioResponseDTO]] = None

    model_config = {
        "from_attributes": True
    }


