import pytest
from tribetactics import create_app, db, bcrypt
import os 
from tribetactics.models import Item, Menu, Restaurant, Role, User, Order
import jwt 
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert roles data
    role1 = Role(name='admin')
    role2 = Role(name='restaurant')
    role3 = Role(name='user')
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)

    # Commit the changes for the roles
    db.session.commit()
    hashed_password = bcrypt.generate_password_hash('password1').decode('utf-8')
    user1 = User(username="test1",
                password=hashed_password,
                email='test1@test.com')
    restaurant1 = Restaurant(name='restaurant 1', owner_id=1)
    db.session.add(user1)
    db.session.add(restaurant1)
    # Commit the changes for the roles
    db.session.commit()
    menu1 = Menu(name='restaurant 1', restaurant_id=1)
    db.session.add(menu1)
    order1 = Order(restaurant_id=1, status='Pending')
    db.session.add(order1)
    user1.roles.append(Role.query.filter_by(name='admin').first())
    db.session.commit()

    item1 = Item(menu_id=1, name='test', price=21)
    db.session.add(item1)
    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture
def get_token(scope='module'):
    token = jwt.encode({'id': 1,
                        'email': 'test1@test.com',
                        'role': 'admin'}, os.environ.get('SECRET_KEY') or 'This Is Secret Key', algorithm='HS256')
    print(token)
    return token
