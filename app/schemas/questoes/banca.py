from pydantic import BaseModel

class BancaRequestDTO(BaseModel):
    nome: str
    
class BancaResponseDTO(BaseModel):
    id: int
    nome: str

    model_config = {
        "from_attributes": True
    }
        
        
        