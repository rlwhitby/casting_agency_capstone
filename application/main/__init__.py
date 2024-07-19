from flask import Blueprint

# Ref: https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
bp = Blueprint("main", __name__)

from application.main import routes
