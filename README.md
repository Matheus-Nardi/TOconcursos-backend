

# TOConcursos API

Uma API desenvolvida para gerenciar um ecossistema completo de preparação para concursos, incluindo questões, cronogramas de estudo e acompanhamento de desempenho dos usuários.

## Stack Utilizada

<span>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</span>

## Rodando Localmente 🖥️

Para executar o projeto em seu ambiente local, siga os passos abaixo.

### Pré-requisitos

  - Python 3.9+
  - Docker e Docker Compose

### Passos

1.  Clone o repositório:

    ```sh
    git clon https://github.com/Matheus-Nardi/TOconcursos-backend
    ```

2.  Entre no diretório do repositório:

    ```sh
    cd toconcursos-backend
    ```

3.  Construa e inicie os containers Docker:

    ```sh
    docker-compose up --build
    ```

4.  A aplicação estará disponível em `http://localhost:8080`.

## Documentação Completa

Para uma visão mais aprofundada do projeto, como requisitos, diagramas e protótipo acesse o pdf

[TOConcursos docs](https://github.com/Matheus-Nardi/TOconcursos-backend/blob/main/app/docs/Documenta%C3%A7%C3%A3o%20TOCONCURSOS.pdf)

## Estrutura de Pastas

A estrutura do projeto foi organizada para manter uma clara separação de responsabilidades, facilitando a manutenção e escalabilidade.

```
/app
    /models         # Define os modelos de dados (SQLAlchemy)
    /repository     # Camada de acesso aos dados do banco
    /routers        # Define os endpoints da API (rotas)
    /schemas        # Define os schemas de validação de dados (Pydantic)
    /services       # Contém a lógica de negócio da aplicação
    /utils          # Funções utilitárias (ex: segurança, autenticação)
    database.py     # Configuração da conexão com o banco de dados
    main.py         # Ponto de entrada da aplicação FastAPI
```
