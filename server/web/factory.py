from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import config
from models import db, User
from utils import mail

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    db.init_app(app)
    Bootstrap(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from main import main
    app.register_blueprint(main)
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
