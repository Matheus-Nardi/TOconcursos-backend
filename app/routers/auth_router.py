from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import SessionLocal
from services.usuarios.usuario_service import UsuarioService
from shared.response import response_dto
from utils.security import decode_access_token
from schemas.auth.auth import LoginRequestDTO, TokenResponseDTO, MeResponseDTO

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(db)

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: UsuarioService = Depends(get_usuario_service)
):
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
        return usuario

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@router.post("/login", response_model=TokenResponseDTO)
def login(
    request: LoginRequestDTO,
    service: UsuarioService = Depends(get_usuario_service),
):
    token = service.authenticate_usuario(request.email, request.senha)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    return response_dto(
        data={"access_token": token, "token_type": "bearer"},
        status="success",
        message="Login realizado com sucesso",
        http_code=status.HTTP_200_OK
    )

@router.get("/me", response_model=MeResponseDTO)
def read_me(current_user: dict = Depends(get_current_user)):
    return response_dto(
        data=current_user,
        status="success",
        message="Usuário autenticado",
        http_code=status.HTTP_200_OK
    )
