"""
schemas.py
Define os modelos Pydantic para validação e serialização dos dados
de entrada (requests) e saída (responses) da API.
"""

from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str

class MovieOut(MovieCreate):
    id: int
    year: str | None = None
    director: str | None = None
    plot: str | None = None
    imdb_rating: str | None = None

    class Config:
        orm_mode = True  # Conversão de ORM objects para JSON automaticamente