from app import app
from flask import render_template, request, session

import models.block_filter_model as filter_models
import models.index_model as models
import constants
from utils import Connect


@app.route('/', methods=['get'])
def index():
    conn = Connect.get_connect()
    df_director = filter_models.get_director(conn)
    df_actor = filter_models.get_actor(conn)
    df_genre = filter_models.get_genre(conn)
    df_sessions = models.get_session(
        conn,
        {
            "search_query": request.args.get('search_query'),
            "start_date": request.args.get('start_date'),
            "end_date": request.args.get('end_date'),
            "director": request.args.get('director'),
            "actor": request.args.get('actor'),
            "genre": request.args.get('genre')
        }
    )
    Connect.close_connect(conn)

    return render_template(
        'index.html',
        current_page='index',
        data={
            "search_query": request.args.get('search_query')
            if request.args.get('search_query') is not None
            else "",
            "start_date": request.args.get('start_date')
            if request.args.get('start_date') is not None
            else constants.start_date,
            "end_date": request.args.get('end_date')
            if request.args.get('end_date') is not None
            else constants.end_date,
            "director": request.args.get('director'),
            "actor": request.args.get('actor'),
            "genre": request.args.get('genre')
        },
        data_limit={
            "date": [constants.current_date, None]
        },

        director=df_director,
        actor=df_actor,
        genre=df_genre,

        sessions=df_sessions,

        int=int,
        len=len
    )
