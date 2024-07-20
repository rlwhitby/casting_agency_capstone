from flask import Blueprint

# Ref: https://flask.palletsprojects.com/en/3.0.x/tutorial/views/
bp = Blueprint("main", __name__)

# Imports are at the bottom of the file to avoid circular imports
# Ref: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  # noqa
from application.main import routes  # noqa
