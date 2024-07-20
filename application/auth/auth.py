import os
import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")


# AuthError Exception
class AuthError(Exception):
    """AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
# Reference: Udacity - Full Stack Nanodegree - Identity and Access Management -
# Identity and Authentication - Lesson 15 Practice: Applying Skills in Flask
# Reference: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py  # noqa
def get_token_auth_header():
    """The get_token_auth_header function obtains the Access Token
    from the Authorization Header.

    Returns:
    header_parts[1] (Any): the token part of the header.

    Raises:
    AuthError: 401, along with an appropriate description, if the token is
    not found or the header is not a bearer token.
    """

    # check if Authorization is in request.headers
    if "Authorization" not in request.headers:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "no authorization header is present in the request.",  # noqa
                "success": False,
            },
            401,
        )
    # get the token
    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")
    # check if token is valid
    if len(header_parts) == 1:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Token not found.",
                "success": False,
            },
            401,
        )
    elif len(header_parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
                "success": False,
            },
            401,
        )
    elif header_parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with 'Bearer'.",  # noqa
                "success": False,
            },
            401,
        )
    return header_parts[1]


# Reference: Udacity - Full Stack Nanodegree - Identity and Access Management -
# Access and Authorization - Lesson 4 Using RBAC in Flask
def check_permissions(permission, payload):
    """The check_permissions function checks for the expected permission in the
    WT payload.

    Args:
    permission: string permission (i.e. 'view:actors')
    payload: decoded jwt payload

    Returns:
    (bool): True, if the expected permission is found in the JWT.

    Raises:
    AuthError: 400, "Permissions not included in JWT.", if "permisions" is not
    included in the JWT.
    AuthError: 403, "unauthorized", if the expected permision is not found in
    the JWT.
    """
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
                "success": False,
            },
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "Permission not found.",
                "success": False,
            },
            403,
        )
    return True


# Reference: Udacity - Full Stack Nanodegree - Identity and Access Management -
# Identity and Authentication - Lesson 15 Practice: Applying Skills in Flask
# Reference: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py  # noqa
def verify_decode_jwt(token):
    """The verify_decode_jwt function takes a json web token form Auth0,
    decodes and verifies it using Auth0 /.well-known/jwks.json.

    Args:
    token (str): a json web token.

    Returns:
    payload (dict[str, Any]): the decoded jwt payload.

    Raises:
    AuthError: 401, along with an appropriate description, if the header
    authorisation is malformed, the token is expired or the claims are invalid.
    AuthError: 400, along with an appropriate description, if the
    authentication token cannot be parsed or an appropriate key cannot
    be found.
    """

    # Get the public key from Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    # Get the header data
    unverified_header = jwt.get_unverified_header(token)

    # Choose the key
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization malformed."
                }, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    # Verify the token
    if rsa_key:
        try:
            # Use the key to validate the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please check the audience and issuer.",  # noqa
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def requires_auth(permission=""):
    """The requires_auth decorator method uses the get_token_auth_header
    method to get the token, decodes the jwt using the verify_decode_jwt
    method and finally uses the check_permissions method to validate claims
    and check the requested permission.

    Args:
    permission: string permission (i.e. 'post:drink').

    Returns:
    decorator: the decorator passes the decoded payload to the
    decorated method.
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
