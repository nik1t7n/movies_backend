import duckdb


def initialize_database():
    conn = duckdb.connect('db/movies_info.db')

    conn.execute("""
        CREATE TABLE IF NOT EXISTS links AS
        SELECT * FROM read_csv_auto('db/data/links.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS genome_scores AS
        SELECT * FROM read_csv_auto('db/data/genome-scores.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS genome_tags AS
        SELECT * FROM read_csv_auto('db/data/genome-tags.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies AS
        SELECT * FROM read_csv_auto('db/data/movies.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings AS
        SELECT * FROM read_csv_auto('db/data/ratings.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tags AS
        SELECT * FROM read_csv_auto('db/data/tags.csv')
    """)

    conn.close()
