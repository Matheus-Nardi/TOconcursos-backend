from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Any, Union, List

def response_dto(
    data: Any = None,
    status: str = "success",
    message: str = "Operation completed successfully",
    http_code: int = 200,
    data_format: str = "json"
):
    if http_code == 204:
        return Response(status_code=http_code)
    
    accepted_formats = ["json"]
    if data_format not in accepted_formats:
        raise ValueError(f"Unsupported data format: {data_format}. Supported formats: {accepted_formats}")

    # Converter objetos Pydantic para dict JSON-serializável
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
    """
    Converte objetos Pydantic, listas de objetos Pydantic ou dicts contendo Pydantic
    para dict JSON-serializável, incluindo datetime em ISO 8601.
    """
    if data is None:
        return None
    elif isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    else:
        return data
