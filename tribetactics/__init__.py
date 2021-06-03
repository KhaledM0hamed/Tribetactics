from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from tribetactics.config import Config
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

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
    from tribetactics.dashboard.routes import dashboard
    from tribetactics.api.routes import api

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(dashboard)
    app.register_blueprint(api)

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###
    return app