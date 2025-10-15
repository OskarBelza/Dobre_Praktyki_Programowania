from __future__ import annotations
from typing import List, Optional
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    PrimaryKeyConstraint,
    Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from zadania.zadanie_15_10.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    genres: Mapped[str] = mapped_column(String, nullable=False)  # np. "Action|Comedy"

    # relacje
    link: Mapped["Link"] = relationship(
        back_populates="movie",
        uselist=False,  # 1-1
        cascade="all, delete-orphan"
    )
    ratings: Mapped[List["Rating"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )
    tags: Mapped[List["Tag"]] = relationship(
        back_populates="movie",
        cascade="all, delete-orphan"
    )


class Link(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True
    )
    imdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tmdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    movie: Mapped[Movie] = relationship(back_populates="link")


class Rating(Base):
    __tablename__ = "ratings"

    userId: Mapped[int] = mapped_column(Integer, nullable=False)
    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False
    )
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="ratings")

    __table_args__ = (
        PrimaryKeyConstraint("userId", "movieId", "timestamp", name="pk_ratings"),
        Index("idx_ratings_movie", "movieId"),
    )


class Tag(Base):
    __tablename__ = "tags"

    userId: Mapped[int] = mapped_column(Integer, nullable=False)
    movieId: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False
    )
    tag: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    movie: Mapped[Movie] = relationship(back_populates="tags")

    __table_args__ = (
        PrimaryKeyConstraint("userId", "movieId", "tag", "timestamp", name="pk_tags"),
        Index("idx_tags_movie", "movieId"),
    )
