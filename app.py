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


@app.route("/events-active")
def events():
    date = datetime.now().date()
    events = query_db('SELECT * FROM Evento WHERE fecha > ?', [date])
    return render_template('events_active.html', events=events)


@app.route("/events-inactive")
def events_inactive():
    date = datetime.now().date()
    events = query_db('SELECT * FROM Evento WHERE fecha <= ?', [date])
    return render_template('events_inactive.html', events=events)


@app.route("/register-event")
def register_event():
    date = datetime.now().date()
    return render_template('register_event.html', date=date)


@app.route("/add-event", methods=['POST'])
def add_event():
    if request.method == 'POST':
        name = request.form["name"]
        date = request.form["date"]
        number = request.form["number"]
        query_db_all_other('INSERT INTO Evento VALUES(NULL,?,?,?,?)', [name, date, number, 0])
        flash('El evento fue agregado satisfactoriamente')
    return redirect(url_for('register_event'))


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
    return redirect(url_for('edit_event', id=id))


@app.route("/selection-event/<id>/<name>")
def select_event(id, name):
    participantes = query_db('SELECT * FROM Participante WHERE evento_id = ?', [id])
    return render_template('select-event.html', id=id, participantes=participantes, name=name)


@app.route("/add-participante/<id>/<name>", methods=['POST'])
def add_participante(id, name):
    if request.method == 'POST':
        name = request.form["name"]
        apellido_materno = request.form["apellido_materno"]
        apellido_paterno = request.form["apellido_paterno"]
        empresa = request.form["empresa"]
        puesto = request.form["puesto"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        date = datetime.now().date()
        numero_asientos = int(query_db('SELECT  numero_asientos_reservados FROM Evento WHERE id = ?  ',
                                       [id], True)["numero_asientos_reservados"])
        numero_asientos = numero_asientos + 1
        print(numero_asientos)
        query_db_all_other('INSERT INTO Participante VALUES(?,?,?,?,?,?,?,?)',
                           [name, apellido_paterno, apellido_materno, empresa, puesto,
                            correo, telefono, id])
        query_db_all_other('INSERT INTO Comprobante VALUES(NULL,?,?,?,?)', [date, "por pagar", id, correo])
        query_db_all_other('UPDATE Evento SET numero_asientos_reservados = ? where id = ?', [numero_asientos, id])
        flash('El participante fue agregado satisfactoriamente')
    return redirect(url_for('select_event', id=id, name=name))


@app.route("/edit-participante/<correo>/<id>/<name>")
def edit_participante(correo, id, name):
    participante = query_db('SELECT * FROM Participante WHERE evento_id = ? and  correo = ? ', [id, correo], True)
    print(participante)
    return render_template('edit_participante.html', participante=participante, name=name, correo=correo, id=id)


@app.route("/update-participante/<correo>/<id>/<name>", methods=['POST'])
def update_participante(correo, id, name):
    if request.method == 'POST':
        name = request.form["name"]
        apellido_materno = request.form["apellido_materno"]
        apellido_paterno = request.form["apellido_paterno"]
        empresa = request.form["empresa"]
        puesto = request.form["puesto"]
        telefono = request.form["telefono"]
        query_db_all_other(
            """UPDATE Participante 
            SET 
            nombre = ?, 
            apellido_paterno = ?, 
            apellido_materno = ?,
            empresa = ?,
            puesto = ?,
            telefono = ?
            WHERE evento_id = ? and  correo = ?""",
            [name, apellido_paterno, apellido_materno, empresa,
             puesto, telefono, id, correo])
        flash('El participante fue actualizado satisfactoriamente')
    return redirect(url_for('edit_participante', correo=correo, id=id, name=name))


@app.route("/comprobante/<correo>/<id>/<name>")
def comprobante(correo, id, name):
    participante = query_db('SELECT * FROM Participante WHERE evento_id = ? and  correo = ? ', [id, correo], True)
    comprobante = query_db('SELECT * FROM Comprobante WHERE evento_id = ? and  participante_correo = ? ',
                           [id, correo], True)
    event = query_db('SELECT * FROM Evento WHERE id  = ?', [id], True)
    return render_template('comprobante.html', participante=participante,
                           comprobante=comprobante, event=event,
                           name=name, correo=correo, id=id)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
