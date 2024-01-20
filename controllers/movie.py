from app import app
from flask import render_template, request, session

import models.block_filter_model as filter_models
import models.movie_model as models
import constants
from utils import Connect


@app.route('/movie', methods=['get'])
def movie():
    session = int(request.args.get('id'))
    category = int(request.args.get('category'))

    if category != 0:
        conn = Connect.get_connect()
        models.add_ticket(conn, session, category)
        Connect.close_connect(conn)

    conn = Connect.get_connect()
    df_sessions = models.get_session(conn, session)
    df_ticket = models.get_ticket(conn, session)
    Connect.close_connect(conn)

    return render_template(
        'movie.html',
        current_page='movie',
        id=session,
        session=df_sessions,
        ticket=df_ticket,
        int=int,
        len=len
    )
