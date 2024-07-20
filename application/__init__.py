from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import os

# Ref: https://testdriven.io/blog/flask-render-deployment/

# ---------------------------
# Configure the Application
# ---------------------------

# Global instances of the Flask extensions, without any arguments passed in.
# These instances are not currently attached to the Flask application.
db = SQLAlchemy()

# ---------------------------
# Create the Application
# ---------------------------


def create_app():
    app = Flask(__name__)

    config_type = os.environ.get(
        "CONFIG_TYPE",
        default="config.DevelopmentConfig"
        )
    app.config.from_object(config_type)

    # Connect the database object to the application instance
    db.init_app(app)

    CORS(app)

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


# models are imported here to avoid circular imports
# Ref: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  # noqa
from application import models  # noqa


def register_blueprints(app):
    from application.errors import bp as errors_bp
    from application.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)
