from http.client import HTTPException
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services.usuarios.usuario_service import UsuarioService
from schemas.usuarios import usuario as schemas
from shared.response import response_dto

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: schemas.UsuarioRequestDTO,
    service: UsuarioService = Depends(get_usuario_service),
):
    created_usuario = service.create_usuario(usuario)
    return response_dto(
        data=created_usuario,
        status="success",
        message="Usuario created successfully",
        http_code=status.HTTP_201_CREATED
    )

@router.get("/{usuario_id}")
def get_usuario_by_id(
    usuario_id: str,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuario = service.get_usuario(usuario_id)
    if usuario:
        return response_dto(
            data=usuario,
            status="success",
            message="Usuario retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Usuario not found",
        http_code=status.HTTP_404_NOT_FOUND
    )

@router.get("/")
def get_all_usuarios(
    skip: int = 0,
    limit: int = 10,
    service: UsuarioService = Depends(get_usuario_service),
):
    usuarios = service.get_all_usuarios(skip=skip, limit=limit)
    return response_dto(
        data=usuarios,
        status="success",
        message="Usuarios retrieved successfully",
        http_code=status.HTTP_200_OK
    )

@router.put("/{usuario_id}")
def update_usuario(
    usuario_id: str,
    usuario: schemas.UsuarioRequestDTO,
    service: UsuarioService = Depends(get_usuario_service),
):
    updated_usuario = service.update_usuario(usuario_id, usuario)
    if updated_usuario:
        return response_dto(
            data=updated_usuario,
            status="success",
            message="Usuario updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Usuario not found",
        http_code=status.HTTP_404_NOT_FOUND
    )

@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: str,
    service: UsuarioService = Depends(get_usuario_service),
):
    if service.delete_usuario(usuario_id):
        return response_dto(
            data=None,
            status="success",
            message="Usuario deleted successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Usuario not found",
        http_code=status.HTTP_404_NOT_FOUND
    )
