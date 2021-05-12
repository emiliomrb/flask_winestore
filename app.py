import os
from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import Venta, NewWine, NewClient, Compra

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Beto'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

############ MODELS #################

class Client(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.Integer)
    #one to many
    order = db.relationship('Sale', backref = 'client', lazy = 'dynamic' )
    

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def  __repr__(self):
        return (f" Cliente: {self.name}")


class Wine(db.Model):

    __tablename__= 'wines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bodega = db.Column(db.String)
    varietal = db.Column(db.String)

    sales = db.relationship('Sale', backref= 'wine', lazy = 'dynamic')
    purchase = db.relationship('Purchase', backref='wine', lazy='dynamic')
    depostito = db.relationship('Warehouse', backref='wine', lazy='dynamic')

    def __init__(self, name, bodega, varietal):
        self.name = name
        self.bodega = bodega
        self.varietal = varietal

    def __repr__(self):
        return (f"{self.id}, {self.name}, {self.varietal}, {self.bodega}")



class Sale(db.Model):
    
    __tablename__= 'sales'

    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    quantity = db.Column(db.Integer)
    amount= db.Column(db. Integer)
    pay_method = db.Column(db.String)
    payment_status = db.Column(db.String)


    def __init__(self, client_id,wine_id, quantity, amount, pay_method, payment_status):
        self.client_id = client_id
        self.wine_id = wine_id
        self.quantity = quantity
        self.amount = amount
        self.pay_method = pay_method
        self.payment_status = payment_status

    def __repr__(self):
        return (f"{self.id} Purchase {self.wine_id}, wasted  {self.amount}")


class Purchase(db.Model):

    __tablename__='purchases'

    id = db.Column(db.Integer, primary_key = True)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    proveedor = db.Column(db.String)
    quantity = db.Column(db.Integer)

    def __init__(self, wine_id, proveedor, quantity):
        self.wine_id = wine_id
        self.proveedor = proveedor
        self.quantity = quantity

    def __repr__(self):
        return 

class Warehouse(db.Model):

    __tablename__='deposito'

    id = db.Column(db.Integer, primary_key=True)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    quantity = db.Column(db.Integer)
    
    def __init__(self,wine_id, quantity):
        self.wine_id = wine_id
        self.quantity = quantity

db.create_all()


############ VIEWS ###############

@app.route('/', methods = ['GET', 'POST'])
def index():

    newbuy = Compra()
    newWine = NewWine()
    form = Venta()
    newcli =NewClient()
    wine_id = False
    client_id = False
    quantity = False
    total = False
    pay_method = False
    payment_status = False

    if "form-submit" in request.form and form.validate_on_submit():
        print (form.validate_on_submit())
        flash(f'Add products,locations and make transfers to view')
        wine_id = form.wine_id.data
        client_id = form.client_id.data
        quantity = form.quantity.data
        total = form.total.data
        pay_method = form.pay_method.data
        payment_status = form.payment_status.data

        venta= Sale(client_id, wine_id, quantity, total, pay_method, payment_status)
     
        db.session.add(venta)
        db.session.commit()

        whare = Warehouse.query.filter_by(wine_id=wine_id).first()
        whare.quantity -= quantity
        db.session.commit()

        form.wine_id.data = ''
        form.client_id.data = ''
        form.quantity.data = ''
        form.total.data = ''
        form.pay_method.data = ''
        form.payment_status.data = ''


    if "form-submit2" in request.form and newWine.validate_on_submit():
        name = newWine.wine_name.data
        varietal = newWine.varietal.data
        bodega = newWine.bodega.data

        vino = Wine(name, bodega, varietal)
        
       
        db.session.add(vino)
        db.session.commit()
        qry = Wine.query.get(vino.id)
        warehouse = Warehouse(qry.id, 0)
        db.session.add(warehouse)
        db.session.commit()


    if "form-submit3" in request.form and newbuy.validate_on_submit():
        
        wine_ids = newbuy.wine_id_b.data
        proveedor = newbuy.proveedor.data
        qttys = newbuy.quantity_b.data
        

        purchase = Purchase(wine_ids, proveedor, qttys)
        query = Warehouse.query.filter_by(wine_id= wine_ids).first()
        query.quantity += qttys
        db.session.add(purchase)
        db.session.commit()

    if "form-submit4" in request.form and newcli.validate_on_submit():
        name = newcli.name.data
        address = newcli.address.data
        phone = newcli.phone.data

        new_client = Client(name, address, phone)
        db.session.add(new_client)
        db.session.commit()
  
    inventory_join = db.session.query(Wine, Warehouse).join(Warehouse).all()
    for wine, warehouse in inventory_join:
        print(wine.id, wine.name, warehouse.quantity)

    return render_template('home.html', inventory_join=inventory_join,  newWine = newWine, newbuy = newbuy, form = form, newcli = newcli)

    









if __name__ == '__main__':
    app.run(debug=True)