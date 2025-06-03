"""
schemas.py
Define os modelos Pydantic para validação e serialização dos dados
de entrada (requests) e saída (responses) da API.
"""

from pydantic import BaseModel

# Modelo para criação de um novo filme, contendo apenas o título obrigatório
class MovieCreate(BaseModel):
    title: str

# Modelo para saída de dados do filme, herdando 'title' e incluindo outros campos opcionais
class MovieOut(MovieCreate):
    id: int                      # Identificador único do filme
    year: str | None = None      # Ano de lançamento (opcional)
    director: str | None = None  # Diretor do filme (opcional)
    plot: str | None = None      # Sinopse do filme (opcional)
    imdb_rating: str | None = None  # Avaliação IMDb (opcional)

    class Config:
        # Permite que objetos ORM (ex: SQLAlchemy) sejam convertidos automaticamente em JSON
        orm_mode = True