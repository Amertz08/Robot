from flask import Flask, render_template
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    from main import main
    app.register_blueprint(main)

    return app