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
    allow_origins=["http://localhost:3000", "https://toconcursos-frontend.vercel.app", "http://152.67.61.34:3000", "http://152.67.61.34.nip.io:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import all_routers
# Base.metadata.create_all(bind=engine)

register_handlers(app)
for router in all_routers:
    app.include_router(router)