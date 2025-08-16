from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Union, List

def response_dto(data: Any = None, status: str = "success", message: str = "Operation completed successfully", http_code: int = 200, data_format: str = "json"):
    accepted_formats = ["json"]
    if data_format not in accepted_formats:
        raise ValueError(f"Unsupported data format: {data_format}. Supported formats: {accepted_formats}")

    # Converter objetos Pydantic para dict
    serialized_data = serialize_data(data)
    
    response = {
        "data": serialized_data,
        "status": status,
        "message": message,
        "http_code": http_code
    }

    if data_format == "json":
        return JSONResponse(response, status_code=http_code, media_type="application/json")

def serialize_data(data: Any) -> Any:
    """Converte objetos Pydantic e listas de objetos Pydantic para dict"""
    if data is None:
        return None
    elif isinstance(data, BaseModel):
        return data.model_dump() 
    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], BaseModel):
        return [item.model_dump() for item in data]
    else:
        return data
