
from fastapi.responses import Response
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.cronograma.cronograma_service import CronogramaService
from schemas.cronograma import cronograma as schemas
from shared.response import response_dto
from shared.get_current_user import get_current_user
from models.usuarios.usuario import Usuario

router = APIRouter(prefix="/cronogramas", tags=["Cronogramas"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cronograma_service(db: Session = Depends(get_db)):
    return CronogramaService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cronograma(
    cronograma: schemas.CronogramaRequestDTO,
    service: CronogramaService = Depends(get_cronograma_service),
    current_user: Usuario = Depends(get_current_user)
):
    created_cronograma = service.create_cronograma(current_user.id, cronograma)
    print(current_user)
    return response_dto(
        data=created_cronograma,
        status="success",
        message="Cronograma created successfully",
        http_code=status.HTTP_201_CREATED
    )



@router.get("/")
def get_all_cronogramas(
    skip: int = 0,
    limit: int = 10,
    service: CronogramaService = Depends(get_cronograma_service),
    current_user: Usuario = Depends(get_current_user)
):
    cronogramas = service.get_all_cronogramas(current_user.id,skip=skip, limit=limit)
    return response_dto(
        data=cronogramas,
        status="success",
        message="Cronogramas retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.get("/{cronograma_id}")
def get_cronograma_by_id(
    cronograma_id: int,
    service: CronogramaService = Depends(get_cronograma_service),
     current_user: Usuario = Depends(get_current_user)
):
    cronograma = service.get_cronograma(current_user.id, cronograma_id)
    if cronograma:
        return response_dto(
            data=cronograma,
            status="success",
            message="Cronograma retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Cronograma not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{cronograma_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cronograma(
    cronograma_id: int,
    service: CronogramaService = Depends(get_cronograma_service),
    current_user: Usuario = Depends(get_current_user)
):
    service.delete_cronograma(current_user.id, cronograma_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)