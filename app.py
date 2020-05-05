import sqlite3
from flask import (
    Flask,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from datetime import datetime

app = Flask(__name__)
DATABASE = './database.db'
app.secret_key = 'mysecretkey'


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


def query_db_all_other(query, args=()):
    """Ejecuta  Las demás consultas:  update, delete, insert"""
    cur = get_db().execute(query, args)
    cur.connection.commit()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/eventos")
def events():
    events = query_db('SELECT * FROM Evento')
    date = datetime.now().date()
    return render_template('events.html', events=events, date=date)


@app.route("/add-event", methods=['POST'])
def add_event():
    if request.method == 'POST':
        name = request.form["name"]
        date = request.form["date"]
        number = request.form["number"]
        query_db_all_other('INSERT INTO Evento VALUES(NULL,?,?,?,?)', [name, date, number, 0])
        flash('El evento fue agregado satisfactoriamente')
    return redirect(url_for('events'))


@app.route("/edit-event/<id>")
def edit_event(id):
    event = query_db('SELECT * FROM Evento WHERE id = ?', [id], True)
    date = datetime.now().date()
    return render_template('edit_event.html', event=event, date=date)


@app.route("/update-event/<id>", methods=['POST'])
def update_event(id):
    if request.method == 'POST':
        name = request.form["name"]
        date = request.form["date"]
        number = request.form["number"]
        query_db_all_other('UPDATE Evento SET nombre = ?, fecha = ?, numero_asientos_total = ? WHERE id = ?',
                           [name, date, number, id])
        flash('El evento fue actualizado satisfactoriamente')
    return redirect(url_for('events'))


@app.route("/selection-event/<id>/<name>")
def select_event(id, name):
    print(id)
    return render_template('select-event.html', allow=True, name=name)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
