from pydantic import BaseModel

class PercentualAcertoPorBanca(BaseModel):
    banca_id: int
    banca_nome: str
    total_questoes: int
    total_acertos: int
    total_erros: int
    percentual_acerto: float

    class Config:
        from_attributes = True

