# ARQUIVO COMENTADO - Router do modelo Historico (será removido)
# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from services.usuarios.historico_service import HistoricoService
# from schemas.usuarios import historico as schemas
# from shared.response import response_dto

# router = APIRouter(prefix="/historicos", tags=["Historicos"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_historico_service(db: Session = Depends(get_db)):
#     return HistoricoService(db)

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_historico(
#     historico: schemas.HistoricoRequestDTO,
#     service: HistoricoService = Depends(get_historico_service),
# ):
#     created_historico = service.create_historico(historico)
#     return response_dto(
#         data=created_historico,
#         status="success",
#         message="Historico created successfully",
#         http_code=status.HTTP_201_CREATED
#     )

# @router.get("/{historico_id}")
# def get_historico_by_id(
#     historico_id: int,
#     service: HistoricoService = Depends(get_historico_service),
# ):
#     historico = service.get_historico(historico_id)
#     if historico:
#         return response_dto(
#             data=historico,
#             status="success",
#             message="Historico retrieved successfully",
#             http_code=status.HTTP_200_OK
#         )
#     return response_dto(
#         data=None,
#         status="error",
#         message="Historico not found",
#         http_code=status.HTTP_404_NOT_FOUND
#     )

# @router.get("/")
# def get_all_historicos(
#     skip: int = 0,
#     limit: int = 10,
#     service: HistoricoService = Depends(get_historico_service),
# ):
#     historicos = service.get_all_historicos(skip=skip, limit=limit)
#     return response_dto(
#         data=historicos,
#         status="success",
#         message="Historicos retrieved successfully",
#         http_code=status.HTTP_200_OK
#     )

# @router.put("/{historico_id}")
# def update_historico(
#     historico_id: int,
#     historico: schemas.HistoricoRequestDTO,
#     service: HistoricoService = Depends(get_historico_service),
# ):
#     updated_historico = service.update_historico(historico_id, historico)
#     if updated_historico:
#         return response_dto(
#             data=updated_historico,
#             status="success",
#             message="Historico updated successfully",
#             http_code=status.HTTP_204_NO_CONTENT
#         )
#     return response_dto(
#         data=None,
#         status="error",
#         message="Historico not found",
#         http_code=status.HTTP_404_NOT_FOUND
#     )

# @router.delete("/{historico_id}")
# def delete_historico(
#     historico_id: int,
#     service: HistoricoService = Depends(get_historico_service),
# ):
#     if service.delete_historico(historico_id):
#         return response_dto(
#             data=None,
#             status="success",
#             message="Historico deleted successfully",
#             http_code=status.HTTP_204_NO_CONTENT
#         )
#     return response_dto(
#         data=None,
#         status="error",
#         message="Historico not found",
#         http_code=status.HTTP_404_NOT_FOUND
#     )
