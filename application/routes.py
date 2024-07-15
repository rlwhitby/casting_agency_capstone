from flask import jsonify

from application import app


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Casting Agency App!"})
