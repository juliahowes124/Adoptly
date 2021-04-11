from models import Pet, db
from app import app

db.drop_all()
db.create_all()

Pet.query.delete()

pet1 = Pet(name='Woof', species="dog", photo_url="https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8ZG9nfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", age="baby", notes="a cute doggo")
pet2 = Pet(name='Porchetta', species="porcupine", photo_url="https://images.unsplash.com/photo-1597284902212-425be320133d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MXx8cG9yY3VwaW5lfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", age="senior")
pet3 = Pet(name='Fluffy', species="cat", photo_url="https://images.unsplash.com/photo-1548247416-ec66f4900b2e?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Nnx8Y2F0fGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", age="young", notes="a fluffy kitty")


db.session.add(pet1)
db.session.add(pet2)
db.session.add(pet3)

db.session.commit()