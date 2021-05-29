import os
from re import S
from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from inventory.forms import AddSale, Submit, Venta, NewWine, NewClient, Compra, PackForm, AddWineToPack, Submit, editproduct, AddSale
from datetime import datetime
from inventory.models import *
from sqlalchemy.exc import IntegrityError

from inventory import db, app 
import jyserver.Flask as jsf




############ VIEWS ###############

@app.route('/ventas1', methods = ['GET', 'POST'])
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

    return render_template('home.html', inventory_join=inventory_join, newbuy = newbuy, form = form, newcli = newcli)

    

@app.route('/products', methods=['GET', 'POST'])
def products():

    newWine = NewWine()
    submit = Submit()
    if "form-submit1" in request.form and newWine.validate_on_submit():
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

    



    inventory_join = db.session.query(Wine, Warehouse).join(Warehouse).all()
    promos = Pack.query.all()

    return render_template('products.html', inventory_join=inventory_join, newWine=newWine, promos = promos, submit=submit)



@app.route('/addpack', methods=['GET', 'POST'])
def packview():

    newpack = PackForm()
    addwinetopack = AddWineToPack()
    wines = []
    qtys= []
    
    
        
    if "form-submit2" in request.form and newpack.validate_on_submit():

        name = newpack.name.data
        date = datetime.now()
        price = newpack.price.data
        cost = 0
        status =  newpack.status.data
        wine_p = newpack.wine_p.data

        for field in newpack.wine_p:
            wine = Pack(name, date, field.wine_id_p.data, field.quantity_p.data, price, status)
            db.session.add(wine)
            db.session.commit()
    promos = Pack.query.all()
    return render_template('addpack.html', newpack=newpack, addwinetopack=addwinetopack, promos = promos)


@app.route('/', methods=['GET'])
def view_home ():
    inventory_join = db.session.query(Wine, Warehouse).join(Warehouse).all()
    return render_template('index.html', inventory_join= inventory_join)

@app.route('/index2', methods=['GET'])
def view_home2 ():
    
    return render_template('index2.html')




@app.route("/Product", methods = ['GET','POST'])
def product():
    form = NewWine()
    eform = editproduct()
    details = Wine.query.all()
    exists = bool(Wine.query.all())
    if exists== False and request.method == 'GET' :
            flash(f'Add products to view','info')

    elif eform.editsubmit.data and eform.validate_on_submit() and request.method == 'POST':

        p_id = request.form.get("productid","")
        pname = request.form.get("productname","")
        details = Wine.query.all()
        prod = Wine.query.filter_by(id = p_id).first()
        prod.name = eform.editname.data
        prod.vaietal= eform.editvarietal.data
        print('id is : '+ str(p_id))
        print(eform.editname.data)
        print (prod.name)
        try:
            db.session.commit()
            flash(f'Your product  has been updated!', 'success')
            return redirect('/Product')
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect('/Product')
        return render_template('product.html',title = 'Products',details=details,eform=eform)
    

    elif form.validate_on_submit() :
        product = Wine(form.wine_name.data, form.varietal.data, form.bodega.data)
        db.session.add(product)        
        try:
            db.session.commit()
            warehouse = Warehouse(product.id, 0)
            db.session.add(warehouse)
            db.session.commit()
            flash(f'Your product {form.wine_name.data} has been added!', 'success')
            return redirect(url_for('product'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect('/Product')
    return render_template('product.html',title = 'Products',eform=eform,form = form,details=details)

@app.route('/ventas' ,methods=['GET','POST'])
def venta():
    saleform = Venta()
    details = Wine.query.all()
    ventas = Sale.query.all()
    addwine = AddSale()

    if request.method =='POST':
        print (request.args)
        print(db.session.query(Client.name).filter(Client.id==2).first())
        sales = {}
        updates =[]
        items = request.form
        print (items)
        '''
        for idx, val in enumerate(addwine.wine.entries):
            sales[idx]= Sale(saleform.client_id.data, val.data['wine'].id, val.data['quantity'], saleform.total.data, saleform.pay_method.data, saleform.payment_status
            .data)
            
            id = val.data['wine'].id
            ware=Warehouse.query.filter_by(wine_id=id).first()
            ware.quantity -= val.data['quantity']
        db.session.add_all(list(sales.values()))
        try:
            db.session.commit()
            flash(f'Your venta {list(sales.values())} has been added!', 'success')
        except IntegrityError:
            return redirect ('/ventas')
            '''
    else:
        search = request.args.get('client')
        print (db.session.query(Client.name).filter(Client.id==search).first())    
    return render_template('ventas.html', saleform=saleform, details = details, ventas = ventas, addwine=addwine)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('client')
    query = db.session.query(Client.name).filter(Client.id==search).first()
    cli_address = db.session.query(Client.address).filter(Client.id==search).first()
    #results = "chajá"
    return jsonify({'result': query, 'c_address': cli_address})

if __name__ == '__main__':
    app.run(debug=True)