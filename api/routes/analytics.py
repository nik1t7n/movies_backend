from typing import List, Dict, Tuple

from fastapi import APIRouter, Depends

from api.dependencies import get_analytics_service
from schemas.schemas import MovieTagsResponse, MovieTitleResponse, MovieResponse, MostRatedMoviesResponse
from services.analytics import AnalyticsService

router = APIRouter()


@router.get(
    "/movies/{movie_title}/titles",
    response_model=MovieTitleResponse,
    summary="Get similar movie titles",
    description="Get all movie titles that consist exactly this title (words)",
)
async def get_movie_titles(
        movie_title: str,
        service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_movie_titles(movie_title)


@router.get(
    "/movies/{movie_title}/tags",
    response_model=MovieTagsResponse,
    summary="Top 3 relevance tags",
    description="Get top 3 tags by relevance for named movie",
)
async def get_movie_tags(
        movie_title: str,
        service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_movie_tags(movie_title)


@router.get(
    "/movies/most_relevant/{tag}",
    response_model=MovieResponse,
    summary="Most relevant movie by tag",
    description="Get the most relevant movie by tag",
)
async def get_most_relevant_movie(
        tag: str,
        service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_most_relevant_movie(tag)


@router.get(
    "/movies/top/most-rated",
    response_model=MostRatedMoviesResponse,
    summary="Most relevant movie by tag",
    description="Get the most relevant movie by tag",
)
async def get_most_rated_movies(
        service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_most_rated_movies()
