from pathlib import Path
from zadania.zadanie_15_10.database import Base, engine, SessionLocal
from zadania.zadanie_15_10.models import Movie, Link, Rating, Tag
from zadania.zadanie_15_10.utils import load_csv

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def main():
    Base.metadata.create_all(bind=engine)  # utwórz tabele jeśli brak

    with SessionLocal() as session:
        n_movies = load_csv(session, Movie,  DATA / "movies.csv",  field_map={"movieId": "id"})
        n_links = load_csv(session, Link,   DATA / "links.csv")
        n_ratings = load_csv(session, Rating, DATA / "ratings.csv")
        n_tags = load_csv(session, Tag,    DATA / "tags.csv")
        print(f"movies={n_movies}, links={n_links}, ratings={n_ratings}, tags={n_tags}")


if __name__ == "__main__":
    main()
