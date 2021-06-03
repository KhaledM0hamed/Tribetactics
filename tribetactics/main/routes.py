from flask import Blueprint, render_template
from flask_login import login_required
from tribetactics.users.utils import admin_required, restaurant_required


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/account')
@login_required
def account():
    return render_template('home.html')