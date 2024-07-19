from flask import Flask
import sqlalchemy as sa
import os

# from config import DevelopmentConfig
from application.extensions import db


# ---------------------------
# Create the Application
# ---------------------------
# TODO: set config_class default as development


# To test - in Render production, can the config_type be passed into create_app()
# or does it have to be fetched from the enviornment variable? - if yes
# refactor to remove config_class and set config_type instead
def create_app():
    app = Flask(__name__)

    # app.config.from_object(config_class)

    # To test - in Render production, can the config_type be passed into create_app()
    # or does it have to be fetched from the enviornment variable? - if yes
    # refactor to remove config_class and set config_type instead
    config_type = os.environ.get("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    # Connect the database object to the application instance
    db.init_app(app)

    # Ref: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
    register_blueprints(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("actors"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Initialized the database!")
    else:
        print("Database already contains the actors table.")

    return app


from application import models


def register_blueprints(app):
    from application.errors import bp as errors_bp
    from application.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
