import duckdb


def initialize_database():
    conn = duckdb.connect('db/movies_info.db')

    conn.execute("""
        CREATE TABLE IF NOT EXISTS links AS
        SELECT * FROM read_csv_auto('data/links.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS genome_scores AS
        SELECT * FROM read_csv_auto('data/genome-scores.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS genome_tags AS
        SELECT * FROM read_csv_auto('data/genome-tags.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies AS
        SELECT * FROM read_csv_auto('data/movies.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings AS
        SELECT * FROM read_csv_auto('data/ratings.csv')
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tags AS
        SELECT * FROM read_csv_auto('data/tags.csv')
    """)

    conn.close()
