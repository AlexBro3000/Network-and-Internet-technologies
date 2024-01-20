from app import app
from flask import render_template

from models.block_database_model import TableDatabase
from utils import Connect


@app.route('/table', methods=['get'])
def table():
    conn = Connect.get_connect()
    df_table = TableDatabase.get_table(
        conn,
        ["Directors", "Actors", "Genres", "Movies", "Halls", "SeatCategories", "Sessions", "Tickets", "MoviesActors", "MoviesGenres", "HallsSeatCategories"]
    )
    Connect.close_connect(conn)

    return render_template(
        'table.html',
        current_page='table',
        tables=df_table,
        len=len
    )
