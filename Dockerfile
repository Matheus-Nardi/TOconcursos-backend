# Imagem base
FROM python:3.13

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

# Copiar entrypoint que executa migrações e sobe a API
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expor porta do FastAPI
EXPOSE 8080

# Usar entrypoint que roda Alembic e depois inicia o uvicorn
ENTRYPOINT ["/entrypoint.sh"]
