"""
main.py
Arquivo principal que inicializa a aplicação FastAPI,
cria as tabelas no banco de dados e registra os endpoints.
"""

from fastapi import FastAPI
from . import crud
from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="OMDb Movies API")

app.include_router(crud.router)