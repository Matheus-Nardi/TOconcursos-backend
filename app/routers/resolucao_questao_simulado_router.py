from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services.usuarios.resolucao_questao_simulado_service import ResolucaoQuestaoSimuladoService
from schemas.usuarios import resolucao_questao_simulado as schemas
from shared.response import response_dto

router = APIRouter(prefix="/resolucoes-simulado", tags=["Resolucoes de Questao em Simulado"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_resolucao_service(db: Session = Depends(get_db)):
    return ResolucaoQuestaoSimuladoService(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_resolucao(resolucao: schemas.ResolucaoQuestaoSimuladoRequestDTO, service: ResolucaoQuestaoSimuladoService = Depends(get_resolucao_service)):
    created = service.create_resolucao(resolucao)
    return response_dto(data=created, status="success", message="Resolucao created successfully", http_code=status.HTTP_201_CREATED)

@router.get("/{resolucao_id}")
def get_resolucao_by_id(resolucao_id: int, service: ResolucaoQuestaoSimuladoService = Depends(get_resolucao_service)):
    resolucao = service.get_resolucao(resolucao_id)
    if resolucao:
        return response_dto(data=resolucao, status="success", message="Resolucao retrieved successfully", http_code=status.HTTP_200_OK)
    return response_dto(data=None, status="error", message="Resolucao not found", http_code=status.HTTP_404_NOT_FOUND)

@router.get("/")
def get_all_resolucoes(skip: int = 0, limit: int = 10, service: ResolucaoQuestaoSimuladoService = Depends(get_resolucao_service)):
    resolucoes = service.get_all_resolucoes(skip=skip, limit=limit)
    return response_dto(data=resolucoes, status="success", message="Resolucoes retrieved successfully", http_code=status.HTTP_200_OK)

@router.put("/{resolucao_id}")
def update_resolucao(resolucao_id: int, resolucao: schemas.ResolucaoQuestaoSimuladoRequestDTO, service: ResolucaoQuestaoSimuladoService = Depends(get_resolucao_service)):
    updated = service.update_resolucao(resolucao_id, resolucao)
    if updated:
        return response_dto(data=updated, status="success", message="Resolucao updated successfully", http_code=status.HTTP_200_OK)
    return response_dto(data=None, status="error", message="Resolucao not found", http_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{resolucao_id}")
def delete_resolucao(resolucao_id: int, service: ResolucaoQuestaoSimuladoService = Depends(get_resolucao_service)):
    if service.delete_resolucao(resolucao_id):
        return response_dto(data=None, status="success", message="Resolucao deleted successfully", http_code=status.HTTP_204_NO_CONTENT)
    return response_dto(data=None, status="error", message="Resolucao not found", http_code=status.HTTP_404_NOT_FOUND)
