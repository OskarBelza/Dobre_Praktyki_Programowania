from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from zadania.zadanie_15_10.database import get_db
from zadania.zadanie_15_10.models import Movie, Link, Rating, Tag
from zadania.zadanie_15_10.utils import list_all


app = FastAPI(title="Movies API")


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return list_all(
        db,
        columns=(Movie.id, Movie.title, Movie.genres),
        order_by=Movie.id,
    )


@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    return list_all(
        db,
        columns=(Link.movieId, Link.imdbId, Link.tmdbId),
        order_by=Link.movieId,
    )


@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    return list_all(
        db,
        columns=(Rating.userId, Rating.movieId, Rating.rating, Rating.timestamp),
        order_by=Rating.movieId,
    )


@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    return list_all(
        db,
        columns=(Tag.userId, Tag.movieId, Tag.tag, Tag.timestamp),
        order_by=Tag.movieId,
    )
