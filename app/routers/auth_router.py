from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import SessionLocal
from services.usuarios.usuario_service import UsuarioService
from services.auth_google.auth_google import AuthGoogleService
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

@router.get("/login/google")
def login_google():
    """
    Inicia o fluxo de autenticação OAuth com Google.
    Redireciona o usuário para a página de autorização do Google.
    """
    try:
        google_service = AuthGoogleService()
        authorization_url = google_service.get_authorization_url()
        return RedirectResponse(url=authorization_url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao iniciar autenticação com Google"
        )

@router.get("/login/google/callback", response_model=TokenResponseDTO)
def login_google_callback(
    code: str = Query(..., description="Código de autorização retornado pelo Google"),
    service: UsuarioService = Depends(get_usuario_service)
):
    """
    Callback do Google OAuth.
    Recebe o código de autorização, troca por token, obtém dados do usuário,
    cria/atualiza usuário no banco e retorna JWT token.
    """
    try:
        google_service = AuthGoogleService()
        user_info = google_service.get_user_info(code)
        
        # Autentica (cria ou atualiza) usuário e gera token JWT
        token = service.authenticate_google_user(user_info)
        
        return response_dto(
            data={"access_token": token, "token_type": "bearer"},
            status="success",
            message="Login com Google realizado com sucesso",
            http_code=status.HTTP_200_OK
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar autenticação com Google: {str(e)}"
        )
