from contextlib import contextmanager

import duckdb


class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = duckdb.connect(self.db_path)
            yield conn
        finally:
            if conn:
                conn.close()
                