"""
Ponto de entrada da aplicação FastAPI.
Inclui configuração para servir frontend HTML e rotas da API.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app import models, database, crud

app = FastAPI()

app.include_router(crud.router)

models.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})