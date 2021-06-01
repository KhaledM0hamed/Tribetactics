from flask import jsonify
from functools import wraps
from tribetactics import db
from tribetactics.models import User
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'user is not authenticated'}), 403
        role = current_user.roles[0]
        if role.name != 'admin':
            return jsonify({'error': 'user is unauthorized'}), 403
        return f(*args, **kwargs)

    return decorated

def restaurant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'user is not authenticated'}), 403
        role = current_user.roles[0]
        if role.name != 'restaurant' and role.name != 'admin':
            return jsonify({'error': 'user is unauthorized'}), 403
        return f(*args, **kwargs)

    return decorated

