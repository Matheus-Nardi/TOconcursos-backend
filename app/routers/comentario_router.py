
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.comentario_service import ComentarioService
from schemas.questoes import comentario as schemas
from shared.response import response_dto
from utils.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.usuarios.usuario_service import UsuarioService
from schemas.usuarios.usuario import UsuarioResponseDTO
from fastapi import Response
router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_comentario_service(db: Session = Depends(get_db)):
    return ComentarioService(db)

def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(db)


bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: UsuarioService = Depends(get_usuario_service)
) -> UsuarioResponseDTO:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        usuario = service.get_usuario(user_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return UsuarioResponseDTO.from_orm(usuario)

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comentario(
    comentario: schemas.ComentarioRequestDTO,
    service: ComentarioService = Depends(get_comentario_service),
    current_user: UsuarioResponseDTO = Depends(get_current_user)
):
    created_comentario = service.create_comentario(comentario, current_user)
    return response_dto(
        data=created_comentario,
        status="success",
        message="Comentario created successfully",
        http_code=status.HTTP_201_CREATED
    )


@router.get("/{comentario_id}")
def get_comentario_by_id(
    comentario_id: int,
    service: ComentarioService = Depends(get_comentario_service),
):
    comentario = service.get_comentario(comentario_id)
    if comentario:
        return response_dto(
            data=comentario,
            status="success",
            message="Comentario retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Comentario not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_comentarios(
    skip: int = 0,
    limit: int = 10,
    service: ComentarioService = Depends(get_comentario_service),
):
    comentarios = service.get_all_comentarios(skip=skip, limit=limit)
    return response_dto(
        data=comentarios,
        status="success",
        message="Comentarios retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{comentario_id}")
def update_comentario(
    comentario_id: int,
    comentario: schemas.ComentarioRequestDTO,
    service: ComentarioService = Depends(get_comentario_service),
    current_user: UsuarioResponseDTO = Depends(get_current_user)
):
    updated_comentario = service.update_comentario(comentario_id, comentario, current_user)
    if updated_comentario:
       return Response(status_code=status.HTTP_204_NO_CONTENT)
    return response_dto(
        data=None,
        status="error",
        message="Comentario not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{comentario_id}")
def delete_comentario(
    comentario_id: int,
    service: ComentarioService = Depends(get_comentario_service),
    current_user: UsuarioResponseDTO = Depends(get_current_user)
):
    service.delete_comentario(comentario_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)