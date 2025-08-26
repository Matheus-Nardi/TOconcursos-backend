from pydantic import BaseModel

class DisciplinaRequestDTO(BaseModel):
    nome: str
    
class DisciplinaResponseDTO(BaseModel):
    id: int
    nome: str

    model_config = {
        "from_attributes": True
    }
        
        
        