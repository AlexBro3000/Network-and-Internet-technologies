import pandas as pd


def get_director(conn):
    return pd.read_sql(f"""
        SELECT
            director_id        AS 'ID',
            director_full_name AS 'Title'
        FROM Directors
        ORDER BY
            director_full_name
    """, conn)


def get_actor(conn):
    return pd.read_sql(f"""
        SELECT
            actor_id        AS 'ID',
            actor_full_name AS 'Title'
        FROM Actors
        ORDER BY
            actor_full_name
    """, conn)


def get_genre(conn):
    return pd.read_sql(f"""
        SELECT
            genre_id   AS 'ID',
            genre_name AS 'Title'
        FROM Genres
        ORDER BY
            genre_name
    """, conn)
