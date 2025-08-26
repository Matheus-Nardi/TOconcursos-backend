
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.orgao_service import OrgaoService
from schemas.questoes import orgao as schemas
from shared.response import response_dto
router = APIRouter(prefix="/orgaos", tags=["Orgaos"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_orgao_service(db: Session = Depends(get_db)):
    return OrgaoService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_orgao(
    orgao: schemas.OrgaoRequestDTO,
    service: OrgaoService = Depends(get_orgao_service),
):
    created_orgao = service.create_orgao(orgao)
    return response_dto(
        data=created_orgao,
        status="success",
        message="Orgao created successfully",
        http_code=status.HTTP_201_CREATED
    )


@router.get("/{orgao_id}")
def get_orgao_by_id(
    orgao_id: int,
    service: OrgaoService = Depends(get_orgao_service),
):
    orgao = service.get_orgao(orgao_id)
    if orgao:
        return response_dto(
            data=orgao,
            status="success",
            message="Orgao retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Orgao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_orgaos(
    skip: int = 0,
    limit: int = 10,
    service: OrgaoService = Depends(get_orgao_service),
):
    orgaos = service.get_all_orgaos(skip=skip, limit=limit)
    return response_dto(
        data=orgaos,
        status="success",
        message="Orgaos retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{orgao_id}")
def update_orgao(
    orgao_id: int,
    orgao: schemas.OrgaoRequestDTO,
    service: OrgaoService = Depends(get_orgao_service),
):
    updated_orgao = service.update_orgao(orgao_id, orgao)
    if updated_orgao:
        return response_dto(
            data=updated_orgao,
            status="success",
            message="Orgao updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Orgao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{orgao_id}")
def delete_orgao(
    orgao_id: int,
    service: OrgaoService = Depends(get_orgao_service),
):
    if service.delete_orgao(orgao_id):
        return response_dto(
            data=None,
            status="success",
            message="Orgao deleted successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Orgao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )