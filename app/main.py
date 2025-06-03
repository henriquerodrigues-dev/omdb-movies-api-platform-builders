"""
Ponto de entrada da aplicação FastAPI.
Inclui configuração para servir frontend HTML e rotas da API.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app import models, database, crud

# Criação da instância principal da aplicação FastAPI
app = FastAPI()

# Inclusão do roteador definido no módulo 'crud' (responsável pelas rotas da API)
app.include_router(crud.router)

# Criação das tabelas no banco de dados com base nos modelos definidos
models.Base.metadata.create_all(bind=database.engine)

# Monta a pasta 'static' para servir arquivos estáticos (ex: CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração do mecanismo de templates usando Jinja2
templates = Jinja2Templates(directory="templates")

# Rota raiz ("/") da aplicação. Renderiza o template HTML inicial
@app.get("/", include_in_schema=False)
def root(request: Request):
    # Retorna o template 'index.html' passando o objeto de requisição
    return templates.TemplateResponse("index.html", {"request": request})
