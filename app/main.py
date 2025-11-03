# app/main.py
from core.handler.exception_handler import register_handlers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from database import engine, Base  # Ajuste o import para onde estão seu engine e Base
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(title="TOConcursos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def on_startup():

#     try:
#         with open("import.sql", "r", encoding="utf-8") as f:
#             sql_script = f.read()

#         with engine.connect() as connection:
#             with connection.begin():
#                 connection.execute(text(sql_script))
        
#         log.info("Script import.sql executado com sucesso.")
    
#     except FileNotFoundError:
#         log.warning("Arquivo import.sql não encontrado. Pulando importação de dados.")
#     except Exception as e:
#         log.error(f"Erro ao executar o script 'import.sql': {e}")
#         # Se falhar aqui, você pode querer parar a execução
#         raise

from routers import all_routers
Base.metadata.create_all(bind=engine)

register_handlers(app)
for router in all_routers:
    app.include_router(router)