#!/bin/sh
set -e

echo "🚀 Rodando migrações Alembic..."
uv run alembic upgrade head || {
  echo "❌ Falha ao executar migrações Alembic. Abortando subida da aplicação."
  exit 1
}

echo "✅ Migrações aplicadas com sucesso. Iniciando API FastAPI..."
uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload


