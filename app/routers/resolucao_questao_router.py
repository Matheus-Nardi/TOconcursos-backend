from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services.usuarios.resolucao_questao_service import ResolucaoQuestaoService
from schemas.usuarios import resolucao_questao as schemas
from shared.response import response_dto

router = APIRouter(prefix="/resolucoes-questoes", tags=["ResolucoesQuestoes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_resolucao_service(db: Session = Depends(get_db)):
    return ResolucaoQuestaoService(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_resolucao(
    resolucao: schemas.ResolucaoQuestaoRequestDTO,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
):
    created_resolucao = service.create_resolucao(resolucao)
    return response_dto(
        data=created_resolucao,
        status="success",
        message="ResolucaoQuestao created successfully",
        http_code=status.HTTP_201_CREATED
    )

@router.get("/{resolucao_id}")
def get_resolucao_by_id(
    resolucao_id: int,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
):
    resolucao = service.get_resolucao(resolucao_id)
    if resolucao:
        return response_dto(
            data=resolucao,
            status="success",
            message="ResolucaoQuestao retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="ResolucaoQuestao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )

@router.get("/")
def get_all_resolucoes(
    skip: int = 0,
    limit: int = 10,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
):
    resolucoes = service.get_all_resolucoes(skip=skip, limit=limit)
    return response_dto(
        data=resolucoes,
        status="success",
        message="ResolucaoQuestao retrieved successfully",
        http_code=status.HTTP_200_OK
    )

@router.put("/{resolucao_id}")
def update_resolucao(
    resolucao_id: int,
    resolucao: schemas.ResolucaoQuestaoRequestDTO,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
):
    updated_resolucao = service.update_resolucao(resolucao_id, resolucao)
    if updated_resolucao:
        return response_dto(
            data=updated_resolucao,
            status="success",
            message="ResolucaoQuestao updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="ResolucaoQuestao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )

@router.delete("/{resolucao_id}")
def delete_resolucao(
    resolucao_id: int,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
):
    if service.delete_resolucao(resolucao_id):
        return response_dto(
            data=None,
            status="success",
            message="ResolucaoQuestao deleted successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="ResolucaoQuestao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )
