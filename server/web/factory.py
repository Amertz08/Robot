from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from config import config
from models import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    Bootstrap(app)

    from main import main
    app.register_blueprint(main)
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
