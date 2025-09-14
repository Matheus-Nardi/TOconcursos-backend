
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.banca_service import BancaService
from schemas.questoes import banca as schemas
from shared.response import response_dto
router = APIRouter(prefix="/bancas", tags=["Bancas"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_banca_service(db: Session = Depends(get_db)):
    return BancaService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_banca(
    banca: schemas.BancaRequestDTO,
    service: BancaService = Depends(get_banca_service),
):
    created_banca = service.create_banca(banca)
    return response_dto(
        data=created_banca,
        status="success",
        message="Banca created successfully",
        http_code=status.HTTP_201_CREATED
    )


@router.get("/{banca_id}")
def get_banca_by_id(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    banca = service.get_banca(banca_id)
    if banca:
        return response_dto(
            data=banca,
            status="success",
            message="Banca retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Banca not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_bancas(
    skip: int = 0,
    limit: int = 10,
    service: BancaService = Depends(get_banca_service),
):
    bancas = service.get_all_bancas(skip=skip, limit=limit)
    return response_dto(
        data=bancas,
        status="success",
        message="Bancas retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{banca_id}")
def update_banca(
    banca_id: int,
    banca: schemas.BancaRequestDTO,
    service: BancaService = Depends(get_banca_service),
):
    updated_banca = service.update_banca(banca_id, banca)
    if updated_banca:
        return response_dto(
            data=updated_banca,
            status="success",
            message="Banca updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Banca not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{banca_id}")
def delete_banca(
    banca_id: int,
    service: BancaService = Depends(get_banca_service),
):
    service.delete_banca(banca_id)
    return response_dto(
        data=None,
        status="success",
        message="Banca deleted successfully",
        http_code=status.HTTP_204_NO_CONTENT
    )