from pydantic import BaseModel, EmailStr

class LoginRequestDTO(BaseModel):
    email: str
    senha: str

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeResponseDTO(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    avatar: str | None = None

    class Config:
        from_attributes = True

class ForgotPasswordRequestDTO(BaseModel):
    email: EmailStr

class ResetPasswordRequestDTO(BaseModel):
    token: str
    new_password: str