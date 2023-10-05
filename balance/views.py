from datetime import date

from flask import redirect, render_template, request, url_for

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


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'GET':
        db = DBManager(RUTA)
        movimiento = db.obtenerMovimiento(id)
        formulario = MovimientoForm(data=movimiento)
        return render_template('form_movimiento.html', form=formulario, id=id)

    if request.method == 'POST':
        form = MovimientoForm(data=request.form)
        if form.validate():
            db = DBManager(RUTA)
            consulta = 'UPDATE movimientos SET fecha=?, concepto=?, tipo=?, cantidad=? WHERE id=?'
            parametros = (
                form.fecha.data,
                form.concepto.data,
                form.tipo.data,
                float(form.cantidad.data),
                form.id.data
            )
            resultado = db.consultaConParametros(consulta, parametros)
            if resultado:
                return redirect(url_for('home'))
            return "El movimiento no se ha podido guardar en la base de datos"
        else:
            return form.errors
