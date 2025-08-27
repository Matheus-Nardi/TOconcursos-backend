from pydantic import BaseModel
from datetime import time
from models.cronograma.dia_da_semana import DiaDaSemanaEnum
from schemas.questoes.disciplina import DisciplinaResponseDTO

class EstudoDiarioRequestDTO(BaseModel):
    hora_inicio: time
    hora_fim: time
    dia_da_semana: DiaDaSemanaEnum
    id_disciplina: int

class EstudoDiarioResponseDTO(BaseModel):
    id: int
    hora_inicio: time
    hora_fim: time
    dia_da_semana: DiaDaSemanaEnum
    disciplina: DisciplinaResponseDTO

    model_config = {
        "from_attributes": True
    }