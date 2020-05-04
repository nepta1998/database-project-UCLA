import sqlite3
from flask import (
    Flask,
    g,
    render_template
)

app = Flask(__name__)
DATABASE = 'database.db'


def make_dicts(cursor, row):
    """
    Muestra los datos obtenidos de la base de datos
    en forma de diccionario en lugar de tupla.
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    """Devuelve la conección de la base de datos"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Cirra la conección cuando termina el request context"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Ejecuta consultas SELECT en la base de datos"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/eventos")
def events():
    return "eventos"


@app.route("/registrar-reserva")
def reserve_register():
    return "registrar reserva"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
