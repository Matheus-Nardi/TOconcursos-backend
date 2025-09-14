from pydantic import BaseModel

class OrgaoRequestDTO(BaseModel):
    label: str
    
class OrgaoResponseDTO(BaseModel):
    id: int
    label: str

    model_config = {
        "from_attributes": True
    }
        
        
        