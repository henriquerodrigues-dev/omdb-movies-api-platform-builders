from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database, omdb

router = APIRouter(prefix="/api")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/movies", response_model=schemas.MovieOut)
async def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.title == movie.title).first()
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    data = await omdb.fetch_movie_data(movie.title)
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Movie not found in OMDb")

    new_movie = models.Movie(
        title=data.get("Title"),
        year=data.get("Year"),
        director=data.get("Director"),
        plot=data.get("Plot"),
        imdb_rating=data.get("imdbRating"),
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.get("/movies/{id}", response_model=schemas.MovieOut)
def get_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).get(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/movies", response_model=list[schemas.MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()
