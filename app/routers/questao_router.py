# app/api/user_routes.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.questao_service import QuestaoService
from schemas.questoes import questao as schemas
from shared.response import response_dto


router = APIRouter(prefix="/questoes", tags=["Questoes"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_questao_service(db: Session = Depends(get_db)):
    return QuestaoService(db)


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_questao(
#     questao: schemas.questaoRequestDTO,
#     service: QuestaoService = Depends(get_questao_service),
# ):
#     created_questao = service.create_questao(questao)
#     return response_dto(
#         data=created_questao,
#         status="success",
#         message="questao created successfully",
#         http_code=status.HTTP_201_CREATED
#     )


@router.get("/{questao_id}")
def get_questao_by_id(
    questao_id: int,
    service: QuestaoService = Depends(get_questao_service),
):
    questao = service.get_questao(questao_id)
    if questao:
        return response_dto(
            data=questao,
            status="success",
            message="questao retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="questao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_questao(
    skip: int = 0,
    limit: int = 10,
    service: QuestaoService = Depends(get_questao_service),
):
    questoes = service.get_all_questao(skip=skip, limit=limit)
    return response_dto(
        data=questoes,
        status="success",
        message="Questao retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{questao_id}")
def update_questao(
    questao_id: int,
    questao: schemas.QuestaoRequestDTO,
    service: QuestaoService = Depends(get_questao_service),
):
    updated_questao = service.update_questao(questao_id, questao)
    if updated_questao:
        return response_dto(
            data=updated_questao,
            status="success",
            message="questao updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="questao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{questao_id}")
def delete_questao(
    questao_id: int,
    service: QuestaoService = Depends(get_questao_service),
):
    if service.delete_questao(questao_id):
        return response_dto(
            data=None,
            status="success",
            message="questao deleted successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="questao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )