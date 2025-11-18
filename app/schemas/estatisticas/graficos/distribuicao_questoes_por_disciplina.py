from pydantic import BaseModel

class DistribuicaoQuestoesPorDisciplina(BaseModel):
    disciplina_id: int
    disciplina_nome: str
    quantidade_questoes: int
    percentual_total: float

    class Config:
        from_attributes = True

