from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from core.exceptions.exception import AppException
from core.schemas.error import ErrorResponse

def register_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
       response_content = ErrorResponse(
            message=exc.details,
            path=str(request.url)
        )
       
       return JSONResponse(
            status_code=exc.status_code,
            content=response_content.model_dump(exclude_none=True)
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
       response_content = ErrorResponse(
            message="Dados inválidos",
            path=str(request.url),
            details=exc.errors()
        )
       return JSONResponse(
            status_code=422,
            content=response_content.model_dump(exclude_none=True)
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        response_content = ErrorResponse(
            message="Ocorreu um erro interno no servidor.",
            path=str(request.url)
        )
        return JSONResponse(
            status_code=500,
            content=response_content.model_dump(exclude_none=True)
        )