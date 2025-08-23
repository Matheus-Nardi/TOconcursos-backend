from pydantic import BaseModel

class AlternativaRequestDTO(BaseModel):
    descricao: str
    is_correta: bool
    questao_id: int

class AlternativaResponseDTO(BaseModel):
    id: int
    descricao: str
    is_correta: bool
    questao_id: int

    model_config = {
        "from_attributes": True
    }