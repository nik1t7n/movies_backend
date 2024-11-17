from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

from repositories.analytics import AnalyticsRepository
from schemas.schemas import MovieTagsResponse, MovieTitleResponse, MovieResponse, MostRatedMoviesResponse, \
    MostRatedMovie, MovieTag


class AnalyticsService:
    def __init__(self, analytics_repository: AnalyticsRepository):
        self.analytics_repository = analytics_repository

    def __get_cover_url_tmdb(self, tmdb_id: int) -> str:
        base_url = "https://www.themoviedb.org/movie/"
        tmdb_url = base_url + str(tmdb_id)

        try:
            response = requests.get(tmdb_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            img_tag = soup.find("img", class_="poster w-full")

            if img_tag and 'src' in img_tag.attrs:
                return img_tag['src']
            raise HTTPException(status_code=404, detail="Poster image not found")
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch poster: {str(e)}")

    def get_movie_titles(self, movie_title: str) -> MovieTitleResponse:
        titles = self.analytics_repository.get_movies_by_title_pattern(movie_title)
        return MovieTitleResponse(titles=titles)

    def get_movie_tags(self, movie_title: str) -> MovieTagsResponse:
        raw_tags = self.analytics_repository.get_movie_tags(movie_title)
        tags = [
            MovieTag(
                movie_title=row[0],
                tag=row[1],
                relevance=row[2]
            )
            for row in raw_tags
        ]
        return MovieTagsResponse(response=tags)

    def get_most_relevant_movie(self, tag: str) -> MovieResponse:
        movie_data = self.analytics_repository.get_movie_by_tag(tag)

        if not movie_data:
            return MovieResponse(
                movie_title="There is no any movies with this tag",
                cover_url="none"
            )

        tmdb_id, movie_title = movie_data
        cover_url = self.__get_cover_url_tmdb(tmdb_id)

        return MovieResponse(
            movie_title=movie_title,
            cover_url=cover_url
        )

    def get_most_rated_movies(self) -> MostRatedMoviesResponse:
        raw_movies = self.analytics_repository.get_top_rated_movies()
        most_rated_movies = [
            MostRatedMovie(
                movie_title=title,
                ratings_count=count,
                cover_url=self.__get_cover_url_tmdb(tmdb_id)
            )
            for tmdb_id, title, count in raw_movies
        ]
        return MostRatedMoviesResponse(most_rated_movies=most_rated_movies)