from flask import Blueprint

# Ref: https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
bp = Blueprint("errors", __name__)

# Imports are at the bottom of the file to avoid circular dependency errors
from application.errors import handlers
