# app/api/user_routes.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.disciplina_service import DisciplinaService
from schemas.questoes import disciplina as schemas
from shared.response import response_dto
router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_disciplina_service(db: Session = Depends(get_db)):
    return DisciplinaService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_disciplina(
    disciplina: schemas.DisciplinaRequestDTO,
    service: DisciplinaService = Depends(get_disciplina_service),
):
    created_disciplina = service.create_disciplina(disciplina)
    return response_dto(
        data=created_disciplina,
        status="success",
        message="Disciplina created successfully",
        http_code=status.HTTP_201_CREATED
    )


@router.get("/{disciplina_id}")
def get_disciplina_by_id(
    disciplina_id: int,
    service: DisciplinaService = Depends(get_disciplina_service),
):
    disciplina = service.get_disciplina(disciplina_id)
    if disciplina:
        return response_dto(
            data=disciplina,
            status="success",
            message="Disciplina retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Disciplina not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/")
def get_all_disciplinas(
    service: DisciplinaService = Depends(get_disciplina_service),
):
    disciplinas = service.get_all_disciplinas()
    return response_dto(
        data=disciplinas,
        status="success",
        message="Disciplinas retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.put("/{disciplina_id}")
def update_disciplina(
    disciplina_id: int,
    disciplina: schemas.DisciplinaRequestDTO,
    service: DisciplinaService = Depends(get_disciplina_service),
):
    updated_disciplina = service.update_disciplina(disciplina_id, disciplina)
    if updated_disciplina:
        return response_dto(
            data=updated_disciplina,
            status="success",
            message="Disciplina updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Disciplina not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{disciplina_id}")
def delete_disciplina(
    disciplina_id: int,
    service: DisciplinaService = Depends(get_disciplina_service),
):

    service.delete_disciplina(disciplina_id)
    return response_dto(
        data=None,
        status="success",
        message="Disciplina deleted successfully",
        http_code=status.HTTP_204_NO_CONTENT
        )