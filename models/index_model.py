import pandas as pd
import constants


def get_session(conn, fltr):
    fltr['search_query'] = fltr['search_query'] if fltr['search_query'] is not None else ""
    fltr['start_date'] = fltr['start_date'] if fltr['start_date'] is not None else constants.start_date
    fltr['end_date'] = fltr['end_date'] if fltr['end_date'] is not None else constants.end_date
    fltr['genre'] = fltr['genre'] if fltr['genre'] is not None and fltr['genre'] != "" else "%"
    fltr['director'] = fltr['director'] if fltr['director'] is not None and fltr['director'] != "" else "%"
    fltr['actor'] = fltr['actor'] if fltr['actor'] is not None and fltr['actor'] != "" else "%"

    sessions = pd.read_sql(f"""
        WITH get_filter(movie_id, director_id, actor_id, genre_id) AS (
            SELECT
                movie_id,
                director_id,
                actor_id,
                genre_id
            FROM Movies AS 'Movie'
                JOIN MoviesActors AS 'MovieActor' USING (movie_id)
                JOIN MoviesGenres AS 'MovieGenre' USING (movie_id)
            WHERE
                Movie.director_id LIKE :director AND
                MovieActor.actor_id LIKE :actor AND
                MovieGenre.genre_id LIKE :genre
            GROUP BY
                movie_id
        )

        SELECT
            Session.session_id          AS 'ID',
            Session.date                AS 'date',
            Movie.movie_img             AS 'img',
            Movie.movie_title           AS 'name',
            Director.director_full_name AS 'director',
            Movie.duration              AS 'duration',
            Movie.movie_description     AS 'description',
            Movie.rating                AS 'rating',
            ""                          AS 'actor',
            ""                          AS 'genre',
            ""                          AS 'time'
        FROM Sessions AS 'Session'
            JOIN Movies AS 'Movie' USING (movie_id)
            JOIN get_filter AS 'Filter' USING (movie_id)
            JOIN Directors AS 'Director' USING (director_id)
        WHERE
            Movie.movie_title LIKE :search_query AND
            Session.date >= :start_date AND Session.date <= :end_date
        GROUP BY
            Session.date, Movie.movie_id
    """, conn, params={
        "search_query": f"%{fltr['search_query']}%",
        "start_date": fltr['start_date'],
        "end_date": fltr['end_date'],
        "director": fltr['director'],
        "actor": fltr['actor'],
        "genre": fltr['genre']
    })
    for i in range(len(sessions)):
        session_id = sessions.loc[i, "ID"]
        sessions.loc[i, "actor"] = get_actor_to_str(conn, session_id)
        sessions.loc[i, "genre"] = get_genre_to_str(conn, session_id)
        sessions.loc[i, "time"] = [[get_time_to_array(conn, session_id)]]
    return sessions


def get_actor_to_str(conn, session_id):
    actor = pd.read_sql("""
        SELECT
            Actor.actor_full_name AS 'name'
        FROM Actors AS 'Actor'
            JOIN MoviesActors AS 'MovieActor' USING (actor_id)
            JOIN Sessions AS 'Session' USING (movie_id)
        WHERE
            Session.session_id == :session_id
    """, conn, params={
        "session_id": int(session_id)
    })
    actor_result = ""
    for i in range(len(actor)):
        name = str(actor.loc[i, "name"])
        actor_result += name + ", "
    return actor_result


def get_genre_to_str(conn, session_id):
    genre = pd.read_sql("""
        SELECT
            Genre.genre_name AS 'name'
        FROM Genres AS 'Genre'
            JOIN MoviesGenres AS 'MovieGenre' USING (genre_id)
            JOIN Sessions AS 'Session' USING (movie_id)
        WHERE
            Session.session_id == :session_id
    """, conn, params={
        "session_id": int(session_id)
    })
    genre_result = ""
    for i in range(len(genre)):
        name = str(genre.loc[i, "name"])
        genre_result += name + ", "
    return genre_result


def get_time_to_array(conn, session_id):
    time = pd.read_sql("""
        WITH get_params(movie_id, date) AS (
            SELECT
                Session.movie_id    AS 'movie_id',
                Session.date        AS 'date'
            FROM Sessions AS 'Session'
            WHERE
                Session.session_id == :session_id
        )
        
        SELECT
            session_id  AS 'ID',
            start_time  AS 'start',
            end_time    AS 'end'
            
        FROM Sessions AS 'Session'
            JOIN get_params AS 'Params'
        WHERE
            Session.movie_id == Params.movie_id AND
            Session.date == Params.date
    """, conn, params={
        "session_id": int(session_id)
    })

    time_result = []
    for i in range(len(time)):
        time_result.append([str(time.loc[i, "start"]), str(time.loc[i, "end"]), int(time.loc[i, "ID"])])
    return time_result
