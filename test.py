from tribetactics import db, create_app
from flask_sqlalchemy import SQLAlchemy
from tribetactics.models import *

try:
    db.create_all(app=create_app())
    print('database created')
except:
    print('database already created before')

db = SQLAlchemy(app=create_app())

user = User(username='khaled',email='shit@gmail.com',password='Khaled123')
role = Role(name='admin')

db.session.add(user)
db.session.commit()
user.roles.append(role)
db.session.add(role)
db.session.commit()

# user = User.query.filter(username='khaled')
restaurant = Restaurant(name='shist', owner_id=user.id)
db.session.add(restaurant)
db.session.commit()

print(user)
print(role)
print(restaurant)
