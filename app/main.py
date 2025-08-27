# app/main.py
from fastapi import FastAPI
from database import Base, engine
from sqlalchemy import text

app = FastAPI(title="TOConcursos API")

@app.on_event("startup")
def on_startup():

    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

   
    print("Iniciando a importação de dados do import.sql...")
    try:
       
        with engine.connect() as connection:
           
            raw_conn = connection.connection
            cursor = raw_conn.cursor()
            with open("import.sql") as f:
        
                cursor.executescript(f.read())
            raw_conn.commit()
        print("Script import.sql executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")
from routers import disciplina_router, orgao_router, instituicao_router, banca_router, questao_router, auth_router, usuario_router

Base.metadata.create_all(bind=engine)


app.include_router(disciplina_router.router)

app.include_router(orgao_router.router)

app.include_router(instituicao_router.router)

app.include_router(banca_router.router)

app.include_router(questao_router.router)

app.include_router(usuario_router.router)

app.include_router(auth_router.router)