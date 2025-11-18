from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import SessionLocal
from utils.security import decode_access_token
from services.usuarios.usuario_service import UsuarioService
from typing import Optional
from schemas.usuarios.usuario import UsuarioResponseDTO

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(db)

bearer_scheme = HTTPBearer()
bearer_scheme_optional = HTTPBearer(auto_error=False)

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

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme_optional),
    service: UsuarioService = Depends(get_usuario_service)
) -> Optional[UsuarioResponseDTO]:
    """
    Retorna o usuário autenticado se houver token válido, caso contrário retorna None.
    Útil para endpoints que funcionam tanto com usuário autenticado quanto não autenticado.
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        if payload is None:
            return None

        user_id = payload.get("sub")
        if user_id is None:
            return None

        usuario = service.get_usuario(user_id)
        return usuario if usuario else None

    except Exception:
        return None