from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required
from tribetactics.users.utils import admin_required, restaurant_required


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)