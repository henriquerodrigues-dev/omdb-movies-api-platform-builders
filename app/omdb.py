"""
omdb.py
Responsável por fazer a requisição assíncrona para a API externa OMDb,
buscando os dados complementares do filme pelo título.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

async def fetch_movie_data(title: str) -> dict:
    """
    Consulta a API OMDb pelo título do filme e retorna o JSON da resposta.
    """
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()