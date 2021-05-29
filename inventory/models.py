import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from inventory import db 

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
    pack = db.relationship('Pack', backref='wine', lazy='dynamic')

    def __init__(self, name, bodega, varietal):
        self.name = name
        self.bodega = bodega
        self.varietal = varietal

    def __repr__(self):
        return (f"{self.name}, id: {self.id}, varietal {self.varietal}, bodega: {self.bodega}")



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
        
class Pack(db.Model):

    __tablename__='packs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime)
    wine_id_p = db.Column(db.Integer, db.ForeignKey('wines.id'))
    quantity_p = db.Column(db.Integer)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    status = db.Column(db.String)

    def __init__(self, name,date, wine_id_p, quantity_p, price, status):
        self.name = name
        self.date = date
        self.wine_id_p = wine_id_p
        self.quantity_p = quantity_p
        self.price = price
        self.status = status

