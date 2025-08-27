
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.instituicao_service import InstituicaoService
from schemas.questoes import instituicao as schemas
from shared.response import response_dto
router = APIRouter(prefix="/instituicaos", tags=["Instituicaos"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_instituicao_service(db: Session = Depends(get_db)):
    return InstituicaoService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_instituicao(
    instituicao: schemas.InstituicaoRequestDTO,
    service: InstituicaoService = Depends(get_instituicao_service),
):
    created_instituicao = service.create_instituicao(instituicao)
    return response_dto(
        data=created_instituicao,
        status="success",
        message="Instituicao created successfully",
        http_code=status.HTTP_201_CREATED
    )


@router.get("/{instituicao_id}")
def get_instituicao_by_id(
    instituicao_id: int,
    service: InstituicaoService = Depends(get_instituicao_service),
):
    instituicao = service.get_instituicao(instituicao_id)
    if instituicao:
        return response_dto(
            data=instituicao,
            status="success",
            message="Instituicao retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Instituicao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_instituicaos(
    skip: int = 0,
    limit: int = 10,
    service: InstituicaoService = Depends(get_instituicao_service),
):
    instituicaos = service.get_all_instituicaos(skip=skip, limit=limit)
    return response_dto(
        data=instituicaos,
        status="success",
        message="Instituicaos retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{instituicao_id}")
def update_instituicao(
    instituicao_id: int,
    instituicao: schemas.InstituicaoRequestDTO,
    service: InstituicaoService = Depends(get_instituicao_service),
):
    updated_instituicao = service.update_instituicao(instituicao_id, instituicao)
    if updated_instituicao:
        return response_dto(
            data=updated_instituicao,
            status="success",
            message="Instituicao updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Instituicao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{instituicao_id}")
def delete_instituicao(
    instituicao_id: int,
    service: InstituicaoService = Depends(get_instituicao_service),
):
    service.delete_instituicao(instituicao_id)
    return response_dto(
        data=None,
        status="success",
        message="Instituicao deleted successfully",
        http_code=status.HTTP_204_NO_CONTENT
        )
