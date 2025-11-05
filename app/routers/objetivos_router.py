
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from shared.response import response_dto
from services.usuarios.objetivo_service import ObjetivoService

router = APIRouter(prefix="/objetivos", tags=["Objetivos"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_objetivo_service(db: Session = Depends(get_db)):
    return ObjetivoService(db)



@router.get("/")
def get_all_objetivos(
    skip: int = 0,
    limit: int = 50,
    service: ObjetivoService = Depends(get_objetivo_service),
):
    objetivos = service.get_all_objetivos(skip=skip, limit=limit)
    return response_dto(
        data=objetivos,
        status="success",
        message="Objetivos retrieved successfully",
        http_code=status.HTTP_200_OK
    )


