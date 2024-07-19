import dateparser
from flask import abort, jsonify, request, current_app

# TODO: may not be needed?
from application.extensions import db

from application.auth.auth import requires_auth
from application.models.enums import GenreEnum

from application.errors.handlers import customExceptionHandler
from application.main import bp
from application.models.models import Actor, Movie


# TODO does this need to be repeated if there are multiple files?
# @bp.after_request
@bp.after_app_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET, PATCH, POST, POST, DELETE, OPTIONS"
    )
    return response


@bp.route("/")
def index():
    return jsonify({"message": "Welcome to the Casting Agency App!"})


# ----------------------------------------------------------------------------#
# Actor Endpoints
# ----------------------------------------------------------------------------#


@bp.route("/actors")
@requires_auth("view:actors")
def get_actors(payload):
    # def get_actors():
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


@bp.route("/actor/<int:actor_id>/movies")
@requires_auth("view:actors")
def get_actor_movies(payload, actor_id):
    # def get_actor_movies(actor_id):
    """Return a list of movies the actor has been cast in.

    The get_actor_movies function uses the GET method to
    list the movies in the movie.format() data representation that
    an actor is cast in, based on the actor_id.
    The endpoint requires the user to have the "view:actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "actor": the actor's name,
    "movies cast in": a list of movies the actor has been cast in.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No actor with id actor_id exists", if the actor_id is not
    in the database.

    HTTPException: 404, "success": False,
    "description": "The actor actor.name has not been cast in any movies yet",
    if the actor has not been cast in any movies.
    """
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404, description="No actor with id " + str(actor_id) + " exists")

        movies = [movie.format() for movie in actor.movies]

        if len(movies) == 0:
            return (
                jsonify(
                    {
                        "success": True,
                        "actor": actor.name,
                        "movies cast in": "The actor "
                        + actor.name
                        + " has not been cast in any movies yet",
                    }
                ),
                200,
            )

        return (
            jsonify({"success": True, "actor": actor.name, "movies cast in": movies}),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/actors/add", methods=["POST"])
@requires_auth("post:actors")
def add_actor(payload):
    # def add_actor():
    """Adds an actor to the database.

    The add_actor endpoint is a private endpoint using the POST method that
    takes a submitted name, age and gender and adds a new actor object to
    the database.

    The endpoint requires the user to have the "post:actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "created": the new actor object in the
    actor.format() data representation.

    Raises:
    HTTPException: 422, "success": False, with a custom "description",
    if the required inputs, name and age, are either not provided, or not
    in the correct format.
    """
    try:
        body = request.get_json()

        # Name is required
        if "name" in body and body.get("name") != "":
            new_name = body.get("name")
        else:
            abort(422, description="An actor's name must be provided")

        # Age is required and muct be a positive integer value
        if "age" in body:
            if isinstance(body.get("age"), int) and body.get("age") > 0:
                new_age = body.get("age")
            else:
                abort(
                    422, description="An actor's age must be a positive integer value"
                )
        else:
            abort(422, description="An actor's age must be provided")

        # Gender is optional
        if "gender" in body:
            new_gender = body.get("gender")
        else:
            new_gender = "None provided"

        actor = Actor(
            name=new_name,
            age=new_age,
            gender=new_gender,
        )

        actor.insert()

        return (
            jsonify(
                {
                    "success": True,
                    "created": actor.format(),
                }
            ),
            201,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/actors/<int:actor_id>/edit", methods=["PATCH"])
@requires_auth("update:actors")
def edit_actor(payload, actor_id):
    # def edit_actor(actor_id):
    """Edits an actor in the database.

    The edit_actor endpoint is a private endpoint using the PATCH method to edit
    a chosen actor from the database.

    The endpoint takes the actor id and, if the actor exists,
    edits it with the submitted name, age and/or gender and
    commits it back to the database.

    The endpoint requires the user to have the "update:actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper and the actor id.

    Returns:
    JSON: "success": True, "actor": the edited actor object in the
    actor.format() data representation.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No actor with id actor_id exists", if the actor_id is not
    in the database.

    HTTPException: 422, "success": False,
    "description": "An actor's age must be a positive integer value",
    if age is provided and is not a positive integer value.
    """

    try:
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404, description="No actor with id " + str(actor_id) + " exists")

        if "name" in body:
            actor.name = body.get("name")
        # Age muct be a positive integer value
        if "age" in body:
            if isinstance(body.get("age"), int) and body.get("age") > 0:
                actor.age = body.get("age")
            else:
                abort(
                    422, description="An actor's age must be a positive integer value"
                )
        if "gender" in body:
            actor.gender = body.get("gender")
        actor.update()

        return (
            jsonify(
                {
                    "success": True,
                    "actor": actor.format(),
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/actors/<int:actor_id>/delete", methods=["DELETE"])
@requires_auth("delete:actors")
def delete_actor(payload, actor_id):
    # def delete_actor(actor_id):
    """Deletes an actor from the database.

    The delete_actor endpoint is a private endpoint using the DELETE method to delete
    a chosen actor from the database.

    The endpoint takes the actor id and, if the actor exists,
    deletes it from the database.

    The endpoint requires the user to have the "delete:actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper and the actor id.

    Returns:
    JSON: "success": True, "deleted id": the deleted actor id.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No actor with id actor_id exists", if the actor id is not
    in the database.
    """
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404, description="No actor with id " + str(actor_id) + " exists")

        actor.delete()

        return (
            jsonify(
                {
                    "success": True,
                    "deleted id": actor_id,
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


# ----------------------------------------------------------------------------#
# Movie Endpoints
# ----------------------------------------------------------------------------#


@bp.route("/movies")
@requires_auth("view:movies")
def get_movies(payload):
    # def get_movies():
    """Returns a list of movies.

    The get_movies function is a private endpoint using the GET method
    that returns a list all the avaliable movies in the agency in the
    movie.format() data representation.
    The endpoint requires the user to have the "view:movies" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "movies": a list of movies.

    Raises:
    HTTPException: 404, "success": False, "description": "There are no movies
    in the database", if there are no movies in the database.
    """
    try:
        allMovies = Movie.query.all()

        if len(allMovies) == 0:
            abort(404, description="There are no movies in the database")

        movies = list(map(lambda movie: movie.format(), allMovies))

        return (
            jsonify(
                {
                    "success": True,
                    "movies": movies,
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/movie/<int:movie_id>/actors")
@requires_auth("view:movies")
def get_movie_actors(payload, movie_id):
    # def get_movie_actors(movie_id):
    """Return a list of actors cast in the actor.

    The get_movie_actors function uses the GET method to
    list the actors in the actor.format() data representation that
    have been cast in the movie, based on the movie_id.
    The endpoint requires the user to have the "view:movies" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "movie": the movie's title,
    "actors cast": a list of actors cast in the movie.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No movie with id movie_id exists", if the movie_id is not
    in the database.

    HTTPException: 404, "success": False,
    "description": "The movie movie.title does not have any cast members yet",
    if the movie does not have any actors cast in it.
    """
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404, description="No movie with id " + str(movie_id) + " exists")

        actors = [actor.format() for actor in movie.actors]

        if len(actors) == 0:
            return (
                jsonify(
                    {
                        "success": True,
                        "movie": movie.title,
                        "actors cast": "The movie "
                        + movie.title
                        + " does not have any cast members yet",
                    }
                ),
                200,
            )

        return jsonify({"success": True, "movie": movie.title, "actors cast": actors})

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/movies/add", methods=["POST"])
@requires_auth("post:movies")
def add_movie(payload):
    # def add_movie():
    """Adds a movie to the database.

    The add_movie endpoint is a private endpoint using the POST method that
    takes a submitted title, release date and genre and adds a new movie
    object to the database.

    The endpoint requires the user to have the "post:movies" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper.

    Returns:
    JSON: "success": True, "created": the new movie object in the
    movie.format() data representation.

    Raises:
    HTTPException: 422, with a custom "description", if the required inputs;
    title, release_date and genre, are either not provided, or not
    in the correct format.

    HTTPException: 422, "message": "A genre from the following list must be entered:
    [the GenrueEnum list]", if the submitted genre does not match an item from the list.
    """
    try:
        body = request.get_json()

        # Movie title is required
        if "title" in body and body.get("title") != "":
            new_title = body.get("title")
        else:
            abort(422, description="A movie's title must be provided")

        # Release Date is required
        # dateparser.parse is used to check if a valid date has been provided
        # Ref: https://dateparser.readthedocs.io/en/latest/settings.html#handling-incomplete-dates
        if "release_date" in body:
            if (
                dateparser.parse(
                    body.get("release_date"),
                    date_formats=["%d-%m-%Y"],
                    settings={"REQUIRE_PARTS": ["day", "month", "year"]},
                )
                == None
            ):
                abort(
                    422,
                    description="The release date must be a valid format e.g. dd-mm-YYYY",
                )
            else:
                new_release_date = body.get("release_date")
        else:
            abort(422, description="A release date must be provided")

        # Genre is required, and must be from the GenreEnum list
        if "genre" in body:
            genre_list = [genre.value for genre in GenreEnum]
            if body.get("genre") in genre_list:
                new_genre = body.get("genre")
            else:
                description = (
                    f"A genre from the following list must be entered: "
                    f"{str(genre_list)}"
                )

                abort(422, description=description)

        else:
            abort(422, description="A genre must be provided")

        movie = Movie(title=new_title, release_date=new_release_date, genre=new_genre)

        movie.insert()

        return (
            jsonify(
                {
                    "success": True,
                    "created": movie.format(),
                }
            ),
            201,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/movies/<int:movie_id>/edit", methods=["PATCH"])
@requires_auth("update:movies")
def edit_movie(payload, movie_id):
    # def edit_movie(movie_id):
    """Edits an movie in the database.

    The edit_movie endpoint is a private endpoint using the PATCH method to edit
    a chosen movie from the database.

    The endpoint takes the movie id and, if the movie exists,
    edits it with the submitted title, release date and/or genre and
    commits it back to the database.

    The endpoint requires the user to have the "update:movies" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper and the movie id.

    Returns:
    JSON: "success": True, "movie": the edited movie object in the
    movie.format() data representation.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No movie with id {movie_id} exists", if the movie_id is not
    in the database.

    HTTPException: 422, "message": "A genre from the following list must be entered:
    [the GenrueEnum list]", if the submitted genre does not match an item from the list.
    """

    try:
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404, description="No movie with id " + str(movie_id) + " exists")

        if "title" in body:
            movie.title = body.get("title")

        if "release_date" in body:
            if (
                dateparser.parse(
                    body.get("release_date"),
                    date_formats=["%d-%m-%Y"],
                    settings={"REQUIRE_PARTS": ["day", "month", "year"]},
                )
                == None
            ):
                abort(
                    422,
                    description="The release date must be a valid format e.g. dd-mm-YYYY",
                )
            else:
                movie.release_date = body.get("release_date")

        if "genre" in body:
            genre_list = [genre.value for genre in GenreEnum]
            if body.get("genre") in genre_list:
                movie.genre = body.get("genre")
            else:
                description = (
                    f"A genre from the following list must be entered: "
                    f"{str(genre_list)}"
                )
                abort(422, description=description)

        movie.update()

        return (
            jsonify(
                {
                    "success": True,
                    "movie": movie.format(),
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


@bp.route("/movies/<int:movie_id>/delete", methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movie(payload, movie_id):
    # def delete_movie(movie_id):
    """Deletes an movie from the database.

    The delete_movie endpoint is a private endpoint using the DELETE method to delete
    a chosen movie from the database.

    The endpoint takes the movie id and, if the movie exists,
    deletes it from the database.

    The endpoint requires the user to have the "delete:movies" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper and the movie id.

    Returns:
    JSON: "success": True, "deleted id": the deleted movie id.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No movie with id movie_id exists", if the movie id is not
    in the database.
    """
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404, description="No movie with id " + str(movie_id) + " exists")

        movie.delete()

        return (
            jsonify(
                {
                    "success": True,
                    "deleted id": movie_id,
                }
            ),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)


# ----------------------------------------------------------------------------#
# Casting Endpoint
# ----------------------------------------------------------------------------#


@bp.route("/movie/<int:movie_id>/actor/<int:actor_id>", methods=["POST"])
@requires_auth("post:cast_actors")
def cast_actor_in_movie(payload, movie_id, actor_id):
    # def cast_actor_in_movie(movie_id, actor_id):
    """Casts an actor in a movie.

    The cast_actor_in_movie endpoint is a private endpoint using the POST method
    cast an actor in a movie using the actor_id and movie_id.

    The endpoint takes the actor_id and movie id and, if the actor and movie both
    exist, links them together.

    The endpoint requires the user to have the "post:cast_actors" permission.

    Args:
    payload (dict[str, Any]): the decoded JWT token from the @requires_auth
    wrapper, the actor_id and the movie id.

    Returns:
    JSON: "success": True, "movie": the movie title, "actor cast": the actor name.

    Raises:
    HTTPException: 404, "success": False,
    "description": "No movie with id movie_id exists", if the movie id is not
    in the database.

    HTTPException: 404, "success": False,
    "description": "No actor with id actor_id exists", if the actor id is not
    in the database.
    """
    try:
        # TODO what about get_or_404? will this remove lines of code?
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404, description="No movie with id " + str(movie_id) + " exists")

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404, description="No actor with id " + str(actor_id) + " exists")

        movie.actors.append(actor)
        movie.insert()

        return (
            jsonify({"success": True, "movie": movie.title, "actor cast": actor.name}),
            200,
        )

    except Exception as e:
        customExceptionHandler(e)
