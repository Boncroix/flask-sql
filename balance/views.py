from flask import render_template

from . import app
from .models import DBManager


@app.route('/')
def home():
    db = DBManager('balance/data/balance.db')
    sql = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos'
    movimientos = db.consultaSQL(sql)

    return render_template('inicio.html', movs=movimientos)
