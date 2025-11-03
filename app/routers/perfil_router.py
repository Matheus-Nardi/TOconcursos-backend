from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.usuarios.perfil_service import PerfilUsuarioService
from schemas.usuarios.perfil_usuario import PerfilUsuarioCompletoDTO
from shared.get_current_user import get_current_user
from services.usuarios.perfil_service import PerfilUsuarioService
from models.usuarios.usuario import Usuario
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(
    prefix="/perfil",
    tags=["Perfil"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_perfil_service(db: Session = Depends(get_db)):
    return PerfilUsuarioService(db)


@router.get("/me", response_model=PerfilUsuarioCompletoDTO, status_code=status.HTTP_200_OK)
def get_perfil_usuario(
    current_user: Usuario = Depends(get_current_user),  # Pode ser usado para verificar permissões
    service: PerfilUsuarioService = Depends(get_perfil_service)
):
    return service.get_perfil_usuario(current_user.id)
