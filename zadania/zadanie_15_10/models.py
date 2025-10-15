from pydantic import BaseModel


class Movie(BaseModel):
    movieId: int
    title: str
    genres: str


class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


class Tag(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


class Link(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: str
