

# is this good practice? find reference
""" The Valid Movie ID and Valid Actor ID constants are set to pass a known valid
id number to the unit test cases that expect them
- GET actor movies
- GET movie actors
- PATCH actor
- PATCH movie
- POST movie actors
- DELETE actor
- DELETE movie

The Invalid Movie ID and Invalid Actor ID constants are set to pass a known invalid
id number to the unit test cases that expect them
- GET actor movies 404 - actor does not exist
- GET movie actors 404
- PATCH actor? or 405 - wrong method or 400 - missing fields?
- PATCH movie? or 405 - wrong method or 400 - missing fields?
- POST movie actors - either movie or actor does not exist
- DELETE actor - actor does not exist
- DELETE movie- movie does not exist

"""
VALID_MOVIE_ID = 1
VALID_ACTOR_ID = 1
INVALID_MOVIE_ID = 1000
INVALID_ACTOR_ID = 1000

VALID_ACTOR = {"name": "Harrison Ford", "age": 81, "gender": "Male"}
INVALID_ACTOR = {"name": "Harrison Ford", "age": 81}

VALID_ACTOR_PATCH = {"name": "Tom Holland", "age": 28, "gender": "Male"}

VALID_MOVIE = {"title": "Raiders of the Lost Ark", "release_date": "1981-06-12", "genre": "Action"}
INVALID_MOVIE = {"title": "Raiders of the Lost Ark", "genre": "Action"}

VALID_MOVIE_PATCH = {"title": "The Impossible", "release_date": "2012-09-09", "genre": "Drama"}

#  VALID_ACTOR_PATCH = {"age": 46}

# curl -X POST http://127.0.0.1:5000/movies
METHOD_NOT_ALLOWED_ERROR = "405: Method Not Allowed"
#TODO: remove
# METHOD_NOT_ALLOWED_MESSAGE = "The method is not allowed for the requested URL."

# curl -d '{"name": "John Doe", "age": 37}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/actors/add
UNPROCESSABLE_ERROR = "422: Unprocessable Entity"
# UNPROCESSABLE_MESSASGE = "The request was well-formed but was unable to be followed due to semantic errors."

NOT_FOUND_ERROR = "404: Not Found"

# Missing data
# curl -d '{"name": "John Doe", "age": "37", "gender": }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/actors/add
BAD_REQUEST_ERROR = "400: Bad Request"
BAD_REQUEST_MESSAGE_START = "Failed to decode JSON object: Expecting value:"
# use assertIn(BAD_REQUEST_MESSAGE_START, data["message"])

UNAUTHORIZED_ERROR = "401: Unauthorized"
UNAUTHORIZED_MESSAGE = ""

FORBIDDEN_ERROR = "403: Forbidden"
UNAUTHORIZED_MESSAGE = ""