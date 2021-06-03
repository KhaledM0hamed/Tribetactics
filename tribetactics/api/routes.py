from flask import Blueprint, current_app, jsonify, request
from .utils import token_required
from tribetactics import bcrypt, db
from tribetactics.models import Restaurant, User, Role, Menu, Order, OrderItems, Item
import jwt

api = Blueprint('api', __name__)

# -*--*--*--*--*--*--*--*--*--*--*-- #
# -*- USER AUTHENTICATION ROUTES -*- #
# -*--*--*--*--*--*--*--*--*--*--*-- #


@api.route('/api/login', methods=['POST'])
def loginUser():
    data = request.get_json(force=True)
    try:
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({"message": "user not found"}), 404

        if bcrypt.check_password_hash(user.password, data['password']):
            token = jwt.encode({'id': user.id,
                                'email': user.email,
                                'role': user.roles[0].name}, current_app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({
                'token': token
            }), 200
        else:
            return jsonify({'message': 'invalid password'}), 403

    except:
        return jsonify({'message': 'user is unauthorized'}), 403


@api.route('/api/register', methods=['POST'])
def registerUser():
    data = request.get_json(force=True)
    user = User.query.filter_by(email=data['email']).first()
    if user is not None:
        return jsonify({"message": "email already exist"}), 409

    user = User.query.filter_by(username=data['username']).first()
    if user is not None:
        return jsonify({"message": "username already exist"}), 409

    hashed_password = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')
    user = User(username=data['username'],
                email=data['email'],
                password=hashed_password)
    db.session.add(user)
    role = Role.query.filter_by(name=data['role']).first()
    if role is None:
        return jsonify({"message": "role not found"}), 404

    user.roles.append(role)
    db.session.commit()

    return jsonify({'message': 'user has been created'}), 200

# -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-- #
# -*--*--*--*--*--*--*- RESTAURANT REQUIRED ROUTES -*--*--*--*--*--*--*- #
# -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-- #
# INCLUDES
# 1. GET restaurants list
# 2. GET restaurant menu
# 3. POST order
# 4. POST order item
# NOTE
# If we follow the standard technique to make a REST API we need
# to make sure we have all CRUD opperations for each resource.
# but due to the lack of time I will implement required operations only.
# -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-- #


@api.route('/api/restaurant')
def getRestaurants():
    try:
        restaurantsQuery = Restaurant.query.all()
        if restaurantsQuery:
            restaurants = []
            for restaurant in restaurantsQuery:
                restaurant_data = {
                    'id': restaurant.id,
                    'name': restaurant.name
                }

                restaurants.append(restaurant_data)
        else:
            return jsonify({'message': 'No restaurant found!'}), 404
    except:
        return jsonify({'message': 'Failed to query'}), 500

    return jsonify({
        'message': restaurants
    }), 200


@api.route('/api/restaurant/<int:restaurant_id>/menu')
def getRestaurantMenu(restaurant_id):
    try:
        menuQuery = Menu.query.filter_by(restaurant_id=restaurant_id).first()
        if len(menuQuery.items) != 0:
            menuItems = []
            for item in menuQuery.items:
                item_data = {
                    'id': item.id,
                    'name': item.name,
                    'price': item.price
                }
                menuItems.append(item_data)
        else:
            return jsonify({'message': []}), 200
    except:
        return jsonify({'message': 'Failed to query'}), 500

    return jsonify({
        'message': menuItems
    }), 200


@api.route('/api/restaurant/<int:restaurant_id>/order', methods=['POST'])
@token_required
def postOrder(current_user, restaurant_id):
    if Restaurant.query.get(restaurant_id) == None:
        return jsonify({"message": "restaurant not found"}), 404

    order = Order(status='Pending', restaurant_id=restaurant_id)
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'order has been created',
                    'id':order.id}), 200

@api.route('/api/restaurant/<int:restaurant_id>/order/<int:order_id>/item/<int:item_id>', methods=['POST'])
@token_required
def postOrderItem(current_user, restaurant_id, order_id, item_id):
    data = request.get_json(force=True)
    if Order.query.get(order_id) == None:
        return jsonify({"message": "Order not found"}), 404
    if Item.query.get(item_id) == None:
        return jsonify({"message": "Item not found"}), 404
    
    orderItem = OrderItems.query.filter_by(item_id=item_id, order_id=order_id).first()
    if orderItem is not None:
        orderItem.quantity += data['quantity']
        db.session.commit()
    else:
        orderItem = OrderItems(item_id=item_id, order_id=order_id, quantity=data['quantity'])
        db.session.add(orderItem)
        db.session.commit()

    return jsonify({'message': 'item has been added!'}), 200
