from pydantic import BaseModel

class PercentualAcertoPorOrgao(BaseModel):
    orgao_id: int
    orgao_nome: str
    total_questoes: int
    total_acertos: int
    total_erros: int
    percentual_acerto: float

    class Config:
        from_attributes = True

