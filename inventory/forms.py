from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FieldList
from wtforms.fields.core import DateField, FieldList, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from inventory.models import Wine



def wines_ids():
        return Wine.query

class AddSale(FlaskForm):
    wine = QuerySelectField('wine id', query_factory=wines_ids)
    quantity = IntegerField('cantidad')
    price = IntegerField('precio')

class Venta(FlaskForm):
    
    client_id = IntegerField('id del cliente')
    name = StringField('nombre')
    address = StringField('domicilio')
    wine_id = FieldList(FormField(AddSale), min_entries=1)
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

class editproduct(FlaskForm):
    editname = StringField('Product Name')
    editvarietal = StringField('Varietal')
    editbodega = StringField('Product Name')
    editsubmit = SubmitField('Save Changes')

class NewClient(FlaskForm):

    name= StringField('nombre')
    address = StringField('domicilio')
    phone = StringField('phone')
    submit= SubmitField()


class AddWineToPack(FlaskForm):
    wine_id_p = IntegerField('id del vino')
    quantity_p = IntegerField('cantidad')

class PackForm(FlaskForm):
  
    name = StringField('nombre del pack')
    
    price = StringField('precio de venta')
    status = StringField('status')
    wine_p = FieldList(FormField(AddWineToPack), min_entries=4)
   



class Submit(FlaskForm):
    submit = SubmitField()
