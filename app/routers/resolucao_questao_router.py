from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
from services.usuarios.resolucao_questao_service import ResolucaoQuestaoService
from schemas.usuarios import resolucao_questao as schemas
from shared.response import response_dto
from shared.get_current_user import get_current_user
from models.usuarios.usuario import Usuario

router = APIRouter(prefix="/resolucoes-questoes", tags=["Resolucoes de Questoes"])

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
    current_user: Usuario = Depends(get_current_user)
):
    created_resolucao = service.create_resolucao(resolucao, current_user.id)
    return response_dto(
        data=created_resolucao,
        status="success",
        message="ResolucaoQuestao created successfully",
        http_code=status.HTTP_201_CREATED
    )

@router.get("/")
def get_all_resolucoes(
    skip: int = 0,
    limit: int = 10,
    service: ResolucaoQuestaoService = Depends(get_resolucao_service),
    current_user: Usuario = Depends(get_current_user)
):
    resolucoes = service.get_all_resolucoes(skip=skip, limit=limit, user_id=current_user.id)
    return response_dto(
        data=resolucoes,
        status="success",
        message="ResolucaoQuestao retrieved successfully",
        http_code=status.HTTP_200_OK
    )
