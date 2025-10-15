import fastapi
from fastapi.responses import Response
import json
from zadania.zadanie_15_10.utils import load_data
from zadania.zadanie_15_10.models import Movie, Rating, Tag, Link
from pathlib import Path

app = fastapi.FastAPI()

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
MOVIES_CSV = DATA_DIR / "movies.csv"
RATINGS_CSV = DATA_DIR / "ratings.csv"
TAGS_CSV = DATA_DIR / "tags.csv"
LINKS_CSV = DATA_DIR / "links.csv"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movies")
def get_movies():
    movies = load_data(MOVIES_CSV, Movie)
    payload = [m.__dict__ for m in movies]
    return Response(
        content=json.dumps(payload, indent=2, ensure_ascii=False),
        media_type="application/json",
    )


@app.get("/links")
def get_links():
    links = load_data(LINKS_CSV, Link)
    payload = [l.__dict__ for l in links]
    return Response(
        content=json.dumps(payload, indent=2, ensure_ascii=False),
        media_type="application/json",
    )


@app.get("/ratings")
def get_ratings():
    ratings = load_data(RATINGS_CSV, Rating)
    payload = [r.__dict__ for r in ratings]
    return Response(
        content=json.dumps(payload, indent=2, ensure_ascii=False),
        media_type="application/json",
    )


@app.get("/tags")
def get_tags():
    tags = load_data(TAGS_CSV, Tag)
    payload = [t.__dict__ for t in tags]
    return Response(
        content=json.dumps(payload, indent=2, ensure_ascii=False),
        media_type="application/json",
    )
