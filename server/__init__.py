from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config.DevConfig)

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from .webhook import bp
    app.register_blueprint(bp)

    from .platform.platform import bp
    app.register_blueprint(bp)

    return app
