from flask import abort, jsonify, current_app
from werkzeug.exceptions import HTTPException

# TODO: is it needed?
from application.extensions import db
from application.errors import bp
from application.auth.auth import AuthError

# ----------------------------------------------------------------------------#
# Error Handling.
# ----------------------------------------------------------------------------#


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


# The app_errorhandler method is used so the the error handlers
# can be defined in a separate blueprint, and still correctly
# return a json response.
# Ref: https://stackoverflow.com/questions/55785287/errorhandler-in-separate-blueprint-is-not-working # noqa
@bp.app_errorhandler(400)
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


@bp.app_errorhandler(404)
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


@bp.app_errorhandler(405)
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


@bp.app_errorhandler(422)
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


@bp.app_errorhandler(500)
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


@bp.app_errorhandler(AuthError)
def auth_error(error):
    """The auth_error error handler returns an appropriate
    json message when an authorization error is raised.

    Args:
    error (Any): The error code passed by the raised AuthError.

    Returns:
    response: The status code and JSON string defined by the
    raised AuthError.
    """
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
