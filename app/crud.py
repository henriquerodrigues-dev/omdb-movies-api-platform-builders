"""
crud.py
Define as operações CRUD para o modelo Movie, incluindo integração
com a API OMDb para buscar dados adicionais ao criar filmes.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database, omdb

# Cria um roteador FastAPI com prefixo '/api' para organizar as rotas
router = APIRouter(prefix="/api")

# Dependência para obter uma sessão de banco de dados e garantir seu fechamento
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/movies", response_model=schemas.MovieOut)
async def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Cria um novo filme na base, buscando dados adicionais na API OMDb.
    Evita duplicidade de títulos.
    """
    # Verifica se o filme já existe no banco pelo título
    db_movie = db.query(models.Movie).filter(models.Movie.title == movie.title).first()
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    # Busca os dados do filme na API OMDb de forma assíncrona
    data = await omdb.fetch_movie_data(movie.title)
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Movie not found in OMDb")

    # Cria uma nova instância do modelo Movie com os dados obtidos
    new_movie = models.Movie(
        title=data.get("Title"),
        year=data.get("Year"),
        director=data.get("Director"),
        plot=data.get("Plot"),
        imdb_rating=data.get("imdbRating"),
    )
    # Adiciona e salva o novo filme no banco de dados
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.get("/movies/{id}", response_model=schemas.MovieOut)
def get_movie(id: int, db: Session = Depends(get_db)):
    """
    Retorna um filme pelo seu ID.
    """
    movie = db.query(models.Movie).get(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/movies", response_model=list[schemas.MovieOut])
def list_movies(db: Session = Depends(get_db)):
    """
    Lista todos os filmes cadastrados no banco.
    """
    return db.query(models.Movie).all()

@router.delete("/movies/{id}", status_code=204)
def delete_movie(id: int, db: Session = Depends(get_db)):
    """
    Remove um filme pelo seu ID.
    """
    movie = db.query(models.Movie).get(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return