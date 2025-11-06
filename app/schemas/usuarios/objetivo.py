from pydantic import BaseModel

class ObjetivoResponseDTO(BaseModel):
    id: int
    nome: str
    area: str
    class Config:
        from_attributes = True
    