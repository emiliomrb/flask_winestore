from app import Client, Purchase, db


q = Client.query.all()
for c in q:
    print(c.id)