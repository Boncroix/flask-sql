from flask import render_template, request

from . import app, RUTA
from .forms import MovimientoForm
from .models import DBManager


@app.route('/')
def home():
    db = DBManager(RUTA)
    sql = 'SELECT id, fecha, concepto, tipo, cantidad FROM movimientos'
    movimientos = db.consultaSQL(sql)
    return render_template('inicio.html', movs=movimientos)

# - Funcion borrar -- DONE
# - Operar con la BD
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
        formulario = MovimientoForm()
        return render_template('form_movimiento.html', form=formulario)
        pass
    return f'TODO: tratar el método POST para actualizar el movimiento {id}'
