from flask import abort, jsonify

from application import app

from application.errors import customExceptionHandler
from application.models import Actor, Movie


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Casting Agency App!"})


# ----------------------------------------------------------------------------#
# Actor Endpoints
# ----------------------------------------------------------------------------#


@app.route("/actors")
# @requires_auth("view:actors")
# def get_actors(payload):
def get_actors():
    """Returns a list of actors.

    The get_actors function is a private endpoint using the GET method
    that returns a list all the avaliable actors in the agency in the
    actor.format() data representation.
    The endpoint requires the user to have the "view:actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "actors": a list of actors.

    Raises:
    HTTPException: 404, "success": False, "description": "There are no actors
    in the database", if there are no actors in the database.
    """
    try:
        allActors = Actor.query.all()

        if len(allActors) == 0:
            # Ref: https://flask.palletsprojects.com/en/2.1.x/errorhandling/
            # Returning API Errors as JSON
            abort(404, description="There are no actors in the database.")

        actors = list(map(lambda actor: actor.format(), allActors))

        return (
            jsonify(
                {
                    "success": True,
                    "actors": actors,
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)
