from flask import current_app
from tribetactics import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    restaurants = db.relationship('Restaurant')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.name}')"


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", back_populates="restaurants")
    menu = db.relationship("Menu", uselist=False, back_populates="restaurant")
    orders = db.relationship("Order", back_populates="restaurant")

    def __repr__(self):
        return f"Restaurant('{self.name}')"


class Menu(db.Model):
    __tablename__= 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    restaurant_id = db.Column(db.Integer(),db.ForeignKey('restaurants.id'))
    restaurant = db.relationship("Restaurant", back_populates="menu")
    items = db.relationship("Item", back_populates="menu")

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float(), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    menu = db.relationship("Menu", back_populates="items")
    orders = db.relationship("OrderItems", back_populates="item")

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default = 'Pending')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship("Restaurant", back_populates="orders")
    # items = db.relationship('Item', secondary='order_items')
    items = db.relationship("OrderItems", back_populates="order")

class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer)
    order = db.relationship('Order', back_populates='items')
    item = db.relationship('Item', back_populates='orders')