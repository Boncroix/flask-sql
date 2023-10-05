from flask_wtf import FlaskForm
from wtforms import (DateField, FloatField, HiddenField, RadioField,
                     StringField, SubmitField)
from wtforms.validators import DataRequired, NumberRange


class MovimientoForm(FlaskForm):
    id = HiddenField()
    fecha = DateField('Fecha', validators=(DataRequired()))
    concepto = StringField('Concepto', validators=(DataRequired()))
    tipo = RadioField(
        choices=[('I', 'Ingreso'), ('G', 'Gasto')], validators=DataRequired())
    cantidad = FloatField('Cantidad', validators=[
        DataRequired(),
        NumberRange(min=0.1, message='No se permiten cantidades inferiores a 10 céntimos')])

    submit = SubmitField('Guardar')
