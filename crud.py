from app import Client, Sale, Wine, db
'''
db.create_all()

vino1 = Wine('mala maria', 'las marias', 'cabernet franc')
vino2 = Wine ( 'sombrero', 'talampaya', 'malbec' )

moni = Client('monica', 'bedoya 123', 111)
soniia = Client ('sonia', 'campiloo 456', 222)
compra6 = Sale(2,2, 3, 1200, 'transferencia', 'pendiente')
#compra5.compras.append(vino1)

db.session.add_all([compra6])
db.session.commit()
'''
join = db.session.query(Sale, Client, Wine).select_from(Sale).join(Client).join(Wine).all()

#for sale, client, wine in join:
# print(client.id, client.name, wine.name, sale.quantity, sale.amount)

gasto_monica = db.session.execute('SELECT amount FROM sales WHERE client_id =1')
gasto_moni = sum([item[0] for item in gasto_monica])
print (gasto_moni)