from tribetactics.models import *
from tribetactics import bcrypt

"""
Example of testing models (coverage isn't 100%)
This test doesn't access the underlying database; 
it only checks the interface class used by SQLAlchemy.
"""

def test_new_user():
    hashed_password = bcrypt.generate_password_hash('testPassword').decode('utf-8')

    user = User(username='testtest',email='testtest@test.com', password=hashed_password)
    assert user.email == 'testtest@test.com'
    assert user.username == 'testtest'
    assert user.password == hashed_password

def test_new_restaurant():
    restaurant = Restaurant(name='test', owner_id=1)
    assert restaurant.owner_id == 1
    assert restaurant.name == 'test'