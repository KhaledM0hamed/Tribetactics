import jwt
from functools import wraps
from flask import jsonify, request, current_app
from tribetactics.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query.get(data['id'])
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator
