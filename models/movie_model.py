import pandas as pd
import constants


def get_session(conn, session_id):
    session = pd.read_sql(f"""
        SELECT
            Session.session_id          AS 'ID',
            Session.date                AS 'date',
            Movie.movie_img             AS 'img',
            Movie.movie_title           AS 'name',
            Director.director_full_name AS 'director',
            Movie.duration              AS 'duration',
            Movie.movie_description     AS 'description',
            Movie.rating                AS 'rating',
            Hall.hall_name              AS 'hall',
            ""                          AS 'actor',
            ""                          AS 'genre',
            ""                          AS 'time'
        FROM Sessions AS 'Session'
            JOIN Movies AS 'Movie' USING (movie_id)
            JOIN Directors AS 'Director' USING (director_id)
            JOIN Halls AS 'Hall' USING (hall_id)
        WHERE
            Session.session_id == :id
    """, conn, params={
        "id": session_id
    })
    for i in range(len(session)):
        session_id = session.loc[i, "ID"]
        session.loc[i, "actor"] = get_actor_to_str(conn, session_id)
        session.loc[i, "genre"] = get_genre_to_str(conn, session_id)
        session.loc[i, "time"] = [[get_time_to_array(conn, session_id)]]
    return session


def get_ticket(conn, session_id):
    return pd.read_sql("""
        SELECT
            Ticket.session_id                   AS 'session',
            Ticket.category_id                  AS 'category',
            Ticket.price                        AS 'price',
            Ticket.available_seats              AS 'available_seats',
            SeatCategorie.category_name         AS 'name',
            SeatCategorie.category_description  AS 'description',
            HallSeatCategorie.number_seats      AS 'number_seats'
        FROM Tickets AS 'Ticket'
            JOIN SeatCategories AS 'SeatCategorie' USING (category_id)
            JOIN Sessions AS 'Session' USING (session_id)
            JOIN HallsSeatCategories AS 'HallSeatCategorie' USING (hall_id,	category_id)
        WHERE
            Ticket.session_id == :id
    """, conn, params={
        "id": session_id
    })


def add_ticket(conn, session, category):
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE Tickets AS 'Ticket'
        SET available_seats = available_seats - 1
        WHERE
            session_id == {session} AND
            category_id == {category} AND
            available_seats > 0
    """)
    conn.commit()


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
