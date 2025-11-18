
from schemas.questoes.filtro_questao import FiltroRequestDTO
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.questoes.questao_service import QuestaoService
from services.questoes.gemini_service import GeminiService
from schemas.questoes import questao as schemas
from schemas.questoes.gemini_resposta import GeminiRespostaResponseDTO
from shared.response import response_dto
from shared.get_current_user import get_current_user_optional
from schemas.usuarios.usuario import UsuarioResponseDTO
from typing import Optional


router = APIRouter(prefix="/questaos", tags=["Questaos"])

# Dependência para o DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_questao_service(db: Session = Depends(get_db)):
    return QuestaoService(db)

def get_gemini_service(db: Session = Depends(get_db)):
    return GeminiService(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_questao(
    questao: schemas.QuestaoRequestDTO,
    service: QuestaoService = Depends(get_questao_service),
):
    created_questao = service.create_questao(questao)
    return response_dto(
        data=created_questao,
        status="success",
        message="Questao created successfully",
        http_code=status.HTTP_201_CREATED
    )





@router.get("/")
def get_all_questaos(
    skip: int = 0,
    limit: int = 10,
    service: QuestaoService = Depends(get_questao_service),
    current_user: Optional[UsuarioResponseDTO] = Depends(get_current_user_optional),
):
    usuario_id = current_user.id if current_user else None
    questaos = service.get_all_questaos(skip=skip, limit=limit, usuario_id=usuario_id)
    return response_dto(
        data=questaos,
        status="success",
        message="Questaos retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.get("/filtros")
def get_all_questaos_filter(
    filtro: FiltroRequestDTO = Depends(),
    skip: int = 0,
    limit: int = 10,
    service: QuestaoService = Depends(get_questao_service),
    current_user: Optional[UsuarioResponseDTO] = Depends(get_current_user_optional),
):
    usuario_id = current_user.id if current_user else None
    questaos = service.filter_questao(filtro=filtro, skip=skip, limit=limit, usuario_id=usuario_id)
    return response_dto(
        data=questaos,
        status="success",
        message="Questaos retrieved successfully",
        http_code=status.HTTP_200_OK
    )

@router.get("/filtros/all")
def get_all_filtros(
    service: QuestaoService = Depends(get_questao_service),
):
    filtros = service.get_filtros()
    return response_dto(
        data=filtros,
        status="success",
        message="Filtros retrieved successfully",
        http_code=status.HTTP_200_OK
    )

@router.get("/{questao_id}")
def get_questao_by_id(
    questao_id: int,
    service: QuestaoService = Depends(get_questao_service),
    current_user: Optional[UsuarioResponseDTO] = Depends(get_current_user_optional),
):
    usuario_id = current_user.id if current_user else None
    questao = service.get_questao(questao_id, usuario_id=usuario_id)
    if questao:
        return response_dto(
            data=questao,
            status="success",
            message="Questao retrieved successfully",
            http_code=status.HTTP_200_OK
        )
    return response_dto(
        data=None,
        status="error",
        message="Questao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/{questao_id}/comentarios")
def get_comentarios_by_questao_id(
    questao_id: int,
    service: QuestaoService = Depends(get_questao_service),
):
    comentarios = service.get_all_comentarios(questao_id)
    return response_dto(
        data=comentarios,
        status="success",
        message="Comentarios retrieved successfully",
        http_code=status.HTTP_200_OK
    )


@router.get("/{questao_id}/gemini-resposta")
def get_gemini_resposta(
    questao_id: int,
    gemini_service: GeminiService = Depends(get_gemini_service),
):
    """
    Gera uma resposta curta e objetiva para a questão usando o Gemini AI.
    
    Args:
        questao_id: ID da questão
        
    Returns:
        Resposta gerada pelo Gemini
    """
    resposta = gemini_service.gerar_resposta_questao(questao_id)
    
    resposta_dto = GeminiRespostaResponseDTO(
        resposta=resposta,
        questao_id=questao_id
    )
    
    return response_dto(
        data=resposta_dto,
        status="success",
        message="Resposta gerada com sucesso",
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
            message="Questao updated successfully",
            http_code=status.HTTP_204_NO_CONTENT
        )
    return response_dto(
        data=None,
        status="error",
        message="Questao not found",
        http_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{questao_id}")
def delete_questao(
    questao_id: int,
    service: QuestaoService = Depends(get_questao_service),
):
    service.delete_questao(questao_id)
    return response_dto(
        data=None,
        status="success",
        message="Questao deleted successfully",
        http_code=status.HTTP_204_NO_CONTENT
        )