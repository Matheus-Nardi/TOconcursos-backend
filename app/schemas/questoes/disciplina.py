from pydantic import BaseModel

class DisciplinaRequestDTO(BaseModel):
    label: str
    
class DisciplinaResponseDTO(BaseModel):
    id: int
    label: str

    model_config = {
        "from_attributes": True
    }
        
        
        