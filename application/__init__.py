from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

from config import Config

# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()

# ---------------------------
# Create the Application
# ---------------------------

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Ref: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
from application import routes, models, errors

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
