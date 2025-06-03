"""
models.py
Define o modelo ORM Movie, representando a tabela movies no banco de dados.
"""

from sqlalchemy import Column, Integer, String
from .database import Base

# Classe que representa a tabela 'movies' no banco de dados
class Movie(Base):
    __tablename__ = "movies"  # Nome da tabela no banco

    # Coluna 'id': chave primária, tipo inteiro, com índice
    id = Column(Integer, primary_key=True, index=True)

    # Coluna 'title': título do filme, único, com índice, obrigatório
    title = Column(String, unique=True, index=True, nullable=False)

    # Coluna 'year': ano de lançamento do filme (opcional)
    year = Column(String, nullable=True)

    # Coluna 'director': diretor do filme (opcional)
    director = Column(String, nullable=True)

    # Coluna 'plot': sinopse do filme (opcional)
    plot = Column(String, nullable=True)

    # Coluna 'imdb_rating': avaliação do IMDb (opcional)
    imdb_rating = Column(String, nullable=True)