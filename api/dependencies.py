from fastapi import Depends

from db.db_conn import DatabaseConnection
from repositories.analytics import AnalyticsRepository
from services.analytics import AnalyticsService


def get_db_connection():
    return DatabaseConnection("db/movies_info.db")


def get_analytics_repository(db_connection: DatabaseConnection = Depends(get_db_connection)):
    return AnalyticsRepository(db_connection)


def get_analytics_service(analytics_repository: AnalyticsRepository = Depends(get_analytics_repository)):
    return AnalyticsService(analytics_repository)
