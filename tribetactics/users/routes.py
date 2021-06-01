from operator import ne
from flask import Blueprint, render_template, flash, redirect, request
from flask.helpers import url_for
from .forms import RegistrationForm, LoginForm
from tribetactics import db, bcrypt
from tribetactics.models import User, Role
from flask_login import login_user, current_user, logout_user
from tribetactics import limiter


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        role = Role.query.get(form.account_type.data)
        user.roles.append(role)
        db.session.commit()
        flash(f'Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@users.route('/login', methods=['POST'])
@limiter.limit("3/5minute")
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessfull. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.errorhandler(429)
def ratelimit_handler(e):
    flash('Too Many Requests. Please Make a new login request after 5 minutes', 'danger')
    return redirect(url_for('users.login'))
