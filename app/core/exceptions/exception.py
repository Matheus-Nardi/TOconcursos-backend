from typing import Any


class AppException(Exception):
    """Exceção base para toda a aplicação."""
    def __init__(self, status_code: int, details: Any = None):
        self.status_code = status_code
        self.details = details


class NotFoundException(AppException):
    """Exceção para recursos não encontrados."""
    def __init__(self, details="Recurso não encontrado"):
        super().__init__(status_code=404, details=details)


class ConflictException(AppException):
    """Exceção para conflitos de recursos (ex: registro duplicado)."""
    def __init__(self, details="Conflito ao processar a requisição"):
        super().__init__(status_code=409, details=details)


class BadRequestException(AppException):
    """Exceção para requisições inválidas."""
    def __init__(self, details="Requisição inválida"):
        super().__init__(status_code=400, details=details)


class UnauthorizedException(AppException):
    """Exceção para falhas de autenticação."""
    def __init__(self, details="Credenciais inválidas"):
        super().__init__(status_code=401, details=details)
