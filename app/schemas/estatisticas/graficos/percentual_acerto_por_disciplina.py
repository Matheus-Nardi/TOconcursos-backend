from pydantic import BaseModel

class PercentualAcertoPorDisciplina(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    total_questoes: int
    total_acertos: int
    total_erros: int
    percentual_acerto: float

    class Config:
        from_attributes = True

