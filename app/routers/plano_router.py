
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.planos.plano_service import PlanoService
from schemas.planos import plano as schemas
from shared.response import response_dto

router = APIRouter(prefix="/planos", tags=["Planos"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_plano_service(db: Session = Depends(get_db)):
    return PlanoService(db)


@router.get("/{plano_id}")
def get_plano_by_id(
    plano_id: int,
    service: PlanoService = Depends(get_plano_service),
):
    plano = service.get_plano(plano_id)
    if plano:
        return response_dto(
            data=plano,
            status="success",
            message="Plano retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Plano not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_planos(
    skip: int = 0,
    limit: int = 10,
    service: PlanoService = Depends(get_plano_service),
):
    planos = service.get_all_planos(skip=skip, limit=limit)
    return response_dto(
        data=planos,
        status="success",
        message="Planos retrieved successfully",
        http_code=status.HTTP_200_OK
    )


