"""
omdb.py
Responsável por fazer a requisição assíncrona para a API externa OMDb,
buscando os dados complementares do filme pelo título.
"""

import httpx
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Recupera a chave da API OMDb a partir das variáveis de ambiente
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

async def fetch_movie_data(title: str) -> dict:
    """
    Consulta a API OMDb pelo título do filme e retorna o JSON da resposta.
    """
    # Monta a URL de requisição com a chave da API e o título do filme
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"

    # Cria um cliente HTTP assíncrono e realiza a requisição
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # Retorna a resposta da API em formato JSON
        return response.json()