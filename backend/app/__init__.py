import os

from flask import Flask
from controllers.main import bp
from database.db import Base, engine

def init_db():
    Base.metadata.create_all(engine)

def create_app(test_config=None):
    init_db()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # TODO: generate randon secret key for prod
        SECRET_KEY='dev',
    )
    
    # register blueprints
    app.register_blueprint(bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app