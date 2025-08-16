# app/main.py
from fastapi import FastAPI
from database import Base, engine
from routers import disciplina_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TOConcursos API")


app.include_router(disciplina_router.router)
