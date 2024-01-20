from flask import Flask

from utils import init_database

app = Flask(__name__)

init_database()

import controllers.index
import controllers.movie
import controllers.table

# { % else %}
# < li class ="{% if current_page == 'table' %}active{% endif %}" >
# < a href = {{url_for("table")}} > Таблицы < / a >
# < / li >