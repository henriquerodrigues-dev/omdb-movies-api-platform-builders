"""
models.py
Define o modelo ORM Movie, representando a tabela movies no banco de dados.
"""

from sqlalchemy import Column, Integer, String
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    year = Column(String, nullable=True)
    director = Column(String, nullable=True)
    plot = Column(String, nullable=True)
    imdb_rating = Column(String, nullable=True)
