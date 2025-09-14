# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar o uv
RUN pip install uv

# Copiar configs do uv
COPY app/pyproject.toml app/uv.lock ./

# Instalar dependências
RUN uv sync --frozen

# Copiar código da aplicação
COPY app/ ./

# Expor porta do FastAPI
EXPOSE 8080

# Rodar a aplicação (via uv)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
