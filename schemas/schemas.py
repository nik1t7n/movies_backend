from typing import List
from pydantic import BaseModel


class MovieBase(BaseModel):
    movie_title: str


class MovieTag(MovieBase):
    tag: str
    relevance: float


class MovieTagsResponse(BaseModel):
    response: List[MovieTag]


class MovieTitleResponse(BaseModel):
    titles: List[str]


class MovieResponse(MovieBase):
    cover_url: str


class MostRatedMovie(MovieBase):
    ratings_count: int
    cover_url: str


class MostRatedMoviesResponse(BaseModel):
    most_rated_movies: List[MostRatedMovie]
