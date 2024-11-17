from typing import Dict, List, Tuple, Optional

import duckdb
from fastapi import HTTPException

from db.db_conn import DatabaseConnection
from schemas.schemas import MovieTagsResponse, MovieTag, MovieTitleResponse, MovieResponse, \
    MostRatedMoviesResponse, MostRatedMovie
import requests
from bs4 import BeautifulSoup


class AnalyticsRepository:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def get_movies_by_title_pattern(self, movie_title: str) -> List[str]:
        query = """
            SELECT title
            FROM movies
            WHERE title LIKE ?
        """

        with self.db_connection.get_connection() as conn:
            try:
                result = conn.execute(query, [f'%{movie_title}%']).fetchall()
                return [title[0] for title in result]
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_movie_tags(self, movie_title: str) -> List[Tuple[str, str, float]]:
        query = """
            SELECT movie_title, tag, relevance 
            FROM (
                SELECT 
                    m.title AS movie_title,
                    sq.tag AS tag,
                    sq.relevance AS relevance,
                    ROW_NUMBER() OVER (PARTITION BY m.title ORDER BY sq.relevance DESC) AS rnk
                FROM (
                    SELECT 
                        gs.movieId AS movieId,
                        gt.tag AS tag,
                        gs.relevance AS relevance
                    FROM genome_tags AS gt
                    INNER JOIN genome_scores AS gs ON gt.tagId = gs.tagId
                    WHERE gs.relevance > 0.3
                ) AS sq
                INNER JOIN movies AS m ON m.movieId = sq.movieId
            ) AS ranked
            WHERE rnk IN (1,2,3) AND movie_title LIKE ?
        """

        with self.db_connection.get_connection() as conn:
            try:
                result = conn.execute(query, [f'%{movie_title}%']).fetchall()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_movie_by_tag(self, tag: str) -> Optional[Tuple[int, str]]:
        query = """
            SELECT l.tmdbId, second_sq.movie_title
            FROM (
                SELECT sq.movieId AS movieId, m.title AS movie_title
                FROM (
                    SELECT gs.movieId AS movieId, t.tag AS tag, gs.relevance AS relevance
                    FROM tags AS t
                    INNER JOIN genome_scores AS gs
                    ON t.movieId = gs.movieId
                    WHERE tag = ?
                    ORDER BY relevance DESC
                    LIMIT 1
                ) AS sq
                INNER JOIN movies AS m
                ON m.movieId = sq.movieId
            ) AS second_sq
            INNER JOIN links AS l
            ON l.movieId = second_sq.movieId
        """

        with self.db_connection.get_connection() as conn:
            try:
                result = conn.execute(query, [tag]).fetchall()
                return result[0] if result else None
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_top_rated_movies(self, limit: int = 10) -> List[Tuple[int, str, int]]:
        query = """
            SELECT l.tmdbId AS tmdbId, sq.movie_title AS movie_title, sq.ratings_count AS ratings_count
            FROM (
                SELECT m.title AS movie_title, COUNT(r.rating) AS ratings_count, m.movieId AS movieId
                FROM movies AS m
                INNER JOIN ratings AS r
                ON m.movieId = r.movieId
                GROUP BY movie_title, m.movieId
                ORDER BY ratings_count DESC
                LIMIT ?
            ) AS sq
            INNER JOIN links AS l
            ON l.movieId = sq.movieId
        """

        with self.db_connection.get_connection() as conn:
            try:
                result = conn.execute(query, [limit]).fetchall()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    # def get_movie_by_genre(self, genre: str):