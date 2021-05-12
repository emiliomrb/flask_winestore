from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class Venta(FlaskForm):

    wine_id = IntegerField('Ingresa el id del vino')
    client_id = IntegerField('id del cliente')
    quantity = IntegerField('cantidad')
    total = IntegerField('total')
    pay_method = StringField('metodo de pago')
    payment_status = StringField('estado')
    submit = SubmitField()

class Compra(FlaskForm):

    wine_id_b = IntegerField('Ingresa el id del vino')
    proveedor = StringField('nombre del proveedor')
    quantity_b = IntegerField('cantidad')
    submit = SubmitField()

class NewWine(FlaskForm):

    wine_name = StringField('nombre del vino')
    varietal = StringField('varietal')
    bodega = StringField('bodega')
    submit = SubmitField()

class NewClient(FlaskForm):

    name= StringField('nombre')
    address = StringField('domicilio')
    phone = StringField('phone')
    submit= SubmitField()