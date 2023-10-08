from datetime import date

from flask import flash, redirect, render_template, request, url_for

from . import RUTA, app
from .forms import BorrarForm, MovimientoForm
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
# TODO: no funciona el metodo de pregunta para borrar
@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'GET':
        form = BorrarForm()
        return render_template('borrado.html', form=form)

    if request.method == 'POST':
        form = BorrarForm()
        if form.cancelar:
            print('hola')
        if form.aceptar.data:
            print('holaaaaaaaaaaaaaaaa')
            db = DBManager(RUTA)
            ha_ido_bien = db.borrar(id)
            if ha_ido_bien:
                flash('El movimiento se ha borrado correctamente',
                      category="exito")
                return redirect(url_for('home'))

    # return render_template('borrado.html')
    # db = DBManager(RUTA)
    # ha_ido_bien = db.borrar(id)
    # if ha_ido_bien:
    #     flash('El movimiento se ha borrado correctamente',
    #           category="exito")
    #     return redirect(url_for('home'))
    # # TODO: en lugar de pintar en mensaje con su propia plantilla, usar un mensaje flash y volver al listado
    # # TODO: un poco más difícil? pedir confirmación antes de eliminar un movimiento:
    # #   - Incluir un texto con la pregunta
    # #   - Incluir un botón aceptar que hace la eliminación y vuelve al listado (con mensaje flash)
    # #   - Incluir un botón cancelar que vuelve al inicio SIN eliminar el movimiento
    # return render_template('borrado.html', resultado=ha_ido_bien)


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
                flash('El movimiento se ha actualizado correctamente',
                      category="exito")
                return redirect(url_for('home'))
            flash('El movimiento no se ha podido guardar en la base de datos',
                  category="error")
            return redirect(url_for('home'))
        else:
            return render_template('form_movimiento.html', form=form, id=id, errors=form.errors)


@app.route('/nuevo', methods=['GET', 'POST'])
def crear_movimiento():
    if request.method == 'GET':
        formulario = MovimientoForm()
        return render_template('nuevo.html', form=formulario)

    if request.method == 'POST':
        form = MovimientoForm()
        if form.validate():
            db = DBManager(RUTA)
            consulta = 'INSERT INTO movimientos (fecha,concepto,tipo,cantidad) VALUES (?,?,?,?)'
            parametros = (
                form.fecha.data,
                form.concepto.data,
                form.tipo.data,
                float(form.cantidad.data)
            )
            resultado = db.consultaConParametros(consulta, parametros)
            if resultado:
                flash('El movimiento se ha registrado correctamente',
                      category="exito")
                return redirect(url_for('home'))
            flash('El movimiento no se ha podido guardar en la base de datos',
                  category="error")
            return redirect(url_for('home'))
        else:
            return render_template('/nuevo.html', form=form, id=id, errors=form.errors)
