import logging

from flask import Flask, render_template
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

    fmt = logging.Formatter(app.config['LOG_FORMAT'])

    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    if not app.debug:
        file_handler = logging.RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(fmt)
        app.logger.addHandler(handler)


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html.j2'), 404

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from main import main
    app.register_blueprint(main)
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from account import acct
    app.register_blueprint(acct, url_prefix='/acct')

    return app
