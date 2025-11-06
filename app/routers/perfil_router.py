from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from services.usuarios.perfil_service import PerfilUsuarioService
from schemas.usuarios.perfil_usuario import PerfilUsuarioCompletoDTO
from schemas.usuarios.usuario import UsuarioUpdateDTO
from schemas.estatisticas.graficos.graficos import GraficosResponseDTO
from shared.get_current_user import get_current_user
from services.usuarios.perfil_service import PerfilUsuarioService
from services.usuarios.usuario_service import UsuarioService
from services.usuarios.estatisticas.graficos.graficos_service import GraficosService
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

def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(db)

def get_graficos_service(db: Session = Depends(get_db)):
    return GraficosService(db)

@router.get("/me", response_model=PerfilUsuarioCompletoDTO, status_code=status.HTTP_200_OK)
def get_perfil_usuario(
    current_user: Usuario = Depends(get_current_user),  # Pode ser usado para verificar permissões
    service: PerfilUsuarioService = Depends(get_perfil_service)
):
    return service.get_perfil_usuario(current_user.id)


@router.patch("/me", status_code=status.HTTP_204_NO_CONTENT)
def update_perfil_usuario(
    update_data: UsuarioUpdateDTO,
    current_user: Usuario = Depends(get_current_user),
    service: UsuarioService = Depends(get_usuario_service)
):
    service.update_usuario(current_user.id, update_data)

@router.post("/me/avatar", status_code=status.HTTP_201_CREATED)
def upload_avatar(
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
    service: PerfilUsuarioService = Depends(get_perfil_service)
):
    return service.upload_avatar(current_user.id, file)

@router.delete("/me/avatar", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(
    current_user: Usuario = Depends(get_current_user),
    service: PerfilUsuarioService = Depends(get_perfil_service)
):
    service.remover_avatar(current_user.id)

@router.get("/me/estatisticas/graficos", response_model=GraficosResponseDTO, status_code=status.HTTP_200_OK)
def estasticas_detalhes(
    current_user: Usuario = Depends(get_current_user),
    service: GraficosService = Depends(get_graficos_service)
):
    quantidade_questoes_por_dia = service.get_quantidade_questoes_por_dia(current_user.id)
    quantidade_certo_errado_por_dia = service.get_quantidade_certo_errado_por_dia(current_user.id)
    
    return GraficosResponseDTO(
        quantidade_questoes_por_dia=quantidade_questoes_por_dia,
        quantidade_certo_errado_por_dia=quantidade_certo_errado_por_dia
    )
