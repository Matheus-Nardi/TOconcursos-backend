import secrets
from sqlalchemy.orm import Session
from models.pagamento.pagamento import Pagamento
from models.pagamento.pix import Pix
from models.pagamento.boleto import Boleto
from models.pagamento.cartao import Cartao
from repository.pagamento.pagamento_repository import PagamentoRepository
from schemas.pagamento.pagamento import PagamentoRequestDTO, PagamentoResponseDTO
from services.planos.plano_service import PlanoService
from repository.usuarios.usuario_repository import UsuarioRepository
from schemas.pagamento import pagamento as schemas
from core.exceptions.exception import NotFoundException, UnauthorizedException

class PagamentoService:
    def __init__(self, db: Session):
        self.repo = PagamentoRepository(db)
        self.plano_service = PlanoService(db)
        self.usuario_repo = UsuarioRepository(db)

    def create_pagamento(self, user_id: int, pagamento: PagamentoRequestDTO) -> PagamentoResponseDTO:
        plano = self.plano_service.get_plano(pagamento.id_plano)
        usuario = self.usuario_repo.get_usuario(user_id)

        if not plano:
            raise NotFoundException("Plano não encontrado")
        
        if pagamento.valor != plano.valor:
            raise UnauthorizedException("Valor do pagamento inválido")
         
        if(pagamento.tipo == "pix"):
           
            db_pagamento = Pix(
                id_plano=pagamento.id_plano,
                valor=pagamento.valor,
                tipo=pagamento.tipo,
                chave_pix="toconconcursos_chave_pix",
                usuario=usuario
            )
        elif(pagamento.tipo == "boleto"):

            db_pagamento = Boleto(
                id_plano=pagamento.id_plano,
                tipo=pagamento.tipo,
                valor=pagamento.valor,
                codigo_barras=self.gerar_codigo_barras_aleatorio(),
                usuario=usuario
            )
        elif(pagamento.tipo == "cartao"):
            db_pagamento = Cartao(
                id_plano=pagamento.id_plano,
                tipo=pagamento.tipo,
                valor=pagamento.valor,
                numero=pagamento.cartao.numero,
                nome_titular=pagamento.cartao.nome_titular,
                validade=pagamento.cartao.validade,
                codigo_seguranca=pagamento.cartao.codigo_seguranca,
                usuario=usuario
            )
        else:
            raise UnauthorizedException("Tipo de pagamento inválido")
        
        db_pagamento = self.repo.create_pagamento(db_pagamento)
        return PagamentoResponseDTO.model_validate(db_pagamento)

    def get_pagamento(self, pagamento_id: int) -> schemas.PagamentoResponseDTO:
        db_pagamento = self.repo.get_pagamento(pagamento_id)
        if not db_pagamento:
            raise NotFoundException("Usuário não encontrado")
        return schemas.PagamentoResponseDTO.model_validate(db_pagamento)

    def get_all_pagamentos(self, skip: int, limit: int) -> list[PagamentoResponseDTO]:
        pagamentos = self.repo.get_all_pagamentos(skip=skip, limit=limit)
        return [PagamentoResponseDTO.model_validate(u) for u in pagamentos]

    def update_pagamento(self, pagamento_id: int, pagamento: PagamentoRequestDTO) -> PagamentoResponseDTO:
        novos_dados = pagamento.model_dump()
        db_pagamento = self.repo.update_pagamento(pagamento_id, novos_dados)
        if not db_pagamento:
            raise NotFoundException("Usuário não encontrado")
        return PagamentoResponseDTO.model_validate(db_pagamento)

    def delete_pagamento(self, pagamento_id: int) -> bool:
        return self.repo.delete_pagamento(pagamento_id)

    def gerar_codigo_barras_aleatorio(self) -> str:
        return ''.join(str(secrets.randbelow(10)) for _ in range(44))