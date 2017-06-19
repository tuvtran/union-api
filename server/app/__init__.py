# server/app/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

# initialize bcrypt
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from app.apis import companies_blueprint, kpi_blueprint
    from app import models      # noqa

    @app.route('/')
    def index():
        return '<h1>Greetings from The Brandery</h1>'

    app.register_blueprint(companies_blueprint)
    app.register_blueprint(kpi_blueprint)
    return app
