from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from tribetactics.config import Config
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    
    from tribetactics.main.routes import main
    from tribetactics.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)
    return app