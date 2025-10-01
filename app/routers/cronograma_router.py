
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
):
    cronogramas = service.get_all_cronogramas(skip=skip, limit=limit)
    return response_dto(
        data=cronogramas,
        status="success",
        message="Cronogramas retrieved successfully",
        http_code=status.HTTP_200_OK
    )


# @router.get("/filtros")
# def get_all_cronogramas_filter(
#     filtro: FiltroRequestDTO = Depends(),
#     skip: int = 0,
#     limit: int = 10,
#     service: CronogramaService = Depends(get_cronograma_service),
# ):
#     cronogramas = service.filter_cronograma(filtro=filtro, skip=skip, limit=limit)
#     return response_dto(
#         data=cronogramas,
#         status="success",
#         message="Cronogramas retrieved successfully",
#         http_code=status.HTTP_200_OK
#     )


@router.get("/{cronograma_id}")
def get_cronograma_by_id(
    cronograma_id: int,
    service: CronogramaService = Depends(get_cronograma_service),
):
    cronograma = service.get_cronograma(cronograma_id)
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

@router.put("/{cronograma_id}")
def update_cronograma(
    cronograma_id: int,
    cronograma: schemas.CronogramaRequestDTO,
    service: CronogramaService = Depends(get_cronograma_service),
):
    updated_cronograma = service.update_cronograma(cronograma_id, cronograma)
    if updated_cronograma:
        return response_dto(
            data=updated_cronograma,
            status="success",
            message="Cronograma updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Cronograma not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{cronograma_id}")
def delete_cronograma(
    cronograma_id: int,
    service: CronogramaService = Depends(get_cronograma_service),
):
    service.delete_cronograma(cronograma_id)
    return response_dto(
        data=None,
        status="success",
        message="Cronograma deleted successfully",
        http_code=status.HTTP_204_NO_CONTENT
        )