from datetime import date
from flask import render_template, request

from . import RUTA, app
from .forms import MovimientoForm
from .models import DBManager


@app.route('/')
def home():
    db = DBManager(RUTA)
    sql = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos'
    movimientos = db.consultaSQL(sql)
    return render_template('inicio.html', movs=movimientos)


# - Función borrar  -- DONE
# - Operar con la BD -- DONE
# - Botón de borrado en cada movimiento -- DONE
# - Plantilla con el resultado -- DONE

@app.route('/borrar/<int:id>')
def eliminar(id):
    db = DBManager(RUTA)
    ha_ido_bien = db.borrar(id)
    return render_template('borrado.html', resultado=ha_ido_bien)


@app.route('/editar/<int:id>')
def actualizar(id):
    if request.method == 'GET':
        db = DBManager(RUTA)
        movimiento = db.editar(id)
        formulario = MovimientoForm(data=movimiento)
        return render_template('form_movimiento.html', form=formulario)
    return f'TODO: tratar el método POST para actualizar el movimiento {id}'


@app.route('/editar1/<int:id>')
def editar(id):
    if request.method == 'GET':
        db = DBManager(RUTA)
        sql = f'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos WHERE id={id}'
        dato = db.consultaSQL(sql)
        dato = dato[0]
        dato['fecha'] = date.fromisoformat(dato['fecha'])
        formulario = MovimientoForm(data=dato)
        return render_template('form_movimiento.html', form=formulario)
    return f'TODO: tratar el método POST para actualizar el movimiento {id}'
