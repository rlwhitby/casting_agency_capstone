from flask import abort, jsonify
from werkzeug.exceptions import HTTPException

from application import app

# ----------------------------------------------------------------------------#
# Error Handling.
# ----------------------------------------------------------------------------#


# The below exception handler function allows any abort() inside
# the try blocks to work while also minimising duplicate code.
# https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour
# https://flask.palletsprojects.com/en/3.0.x/errorhandling/#error-handlers
def customExceptionHandler(e):
    """The customExceptionHandler function aborts the appplication and returns
    an appropriate json message when an HTTPException error is raised.

    Returns a 500 Internal Server Error if a non-HTTP Exception is caught.

    """
    if isinstance(e, HTTPException):
        # If the error has a unique message passed as a description parameter,
        # it will be passed through to the error handler
        # If no description parameter is defined, if will pass the default
        # error message
        abort(e.code, e.description)
    else:
        # HTTPException 500 raised as per advice in this knowledge
        # article https://knowledge.udacity.com/questions/325456.
        abort(500)


# @app.errorhandler(400)
# @app.errorhandler(404)
# @app.errorhandler(405)
# @app.errorhandler(422)
# @app.errorhandler(500)
# def http_error_handler(error):
#     """Returns "success": False, and error code and name, and an
#     error message.
#     """

#     return (
#         jsonify(
#             {
#                 "success": False,
#                 "error": f"{error.code} {error.name}",
#                 "message": error.description,
#             }
#         ),
#         error.code,
#     )


@app.errorhandler(400)
def bad_request(error):
    """Returns "success": False, "error": "400 Bad Request", and an
    error message.
    """

    return (
        jsonify(
            {
                "success": False,
                "error": f"{error.code} {error.name}",
                "message": error.description,
            }
        ),
        400,
    )


@app.errorhandler(404)
def not_found(error):
    """Returns "success": False, "error": "404 Not Found", and an
    error message.
    """

    return (
        jsonify(
            {
                "success": False,
                "error": f"{error.code} {error.name}",
                "message": error.description,
            }
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    """Returns "success": False, "405 Method Not Allowed", and an
    error message.
    """
    return (
        jsonify(
            {
                "success": False,
                "error": f"{error.code}: {error.name}",
                "message": error.description,
            }
        ),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    """Returns "success": False, "error": "422 Unprocessable Content", and an
    error message.
    """
    return (
        jsonify(
            {
                "success": False,
                "error": f"{error.code}: {error.name}",
                "message": error.description,
            }
        ),
        422,
    )


@app.errorhandler(500)
def internal_server_error(error):
    """Returns "success": False, "error": "500 Internal Server Error", and an
    error message.
    """
    return (
        jsonify(
            {
                "success": False,
                "error": f"{error.code}: {error.name}",
                "message": error.description,
            }
        ),
        500,
    )


# @app.errorhandler(AuthError)
# def auth_error(error):
#     """The auth_error error handler returns an appropriate
#     json message when an authorization error is raised.

#     Args:
#     error (Any): The error code passed by the raised AuthError.

#     Returns:
#     response: The status code and JSON string defined by the
#     raised AuthError.
#     """
#     response = jsonify(error.error)
#     response.status_code = error.status_code
#     return response
