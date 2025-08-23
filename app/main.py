# app/main.py
from fastapi import FastAPI
from database import Base, engine
from sqlalchemy import text

# with engine.connect() as conn:
#     with open("import.sql") as f:
#         sql_script = f.read()
#     for statement in sql_script.split(';'):
#         stmt = statement.strip()
#         if stmt:
#             conn.execute(text(stmt))
#     conn.commit()

from routers import disciplina_router, questao_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TOConcursos API")

app.include_router(disciplina_router.router)
app.include_router(questao_router.router)