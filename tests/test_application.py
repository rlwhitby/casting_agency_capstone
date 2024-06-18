# Standard library imports
import os
import unittest
import json
# Third party imports
from flask_sqlalchemy import SQLAlchemy
# Local application imports
from app import create_app
from models import setup_db, Movie, Actor
from test_constants import *

# Find reference for this part of setup
#https://knowledge.udacity.com/questions/972850
# tokens exist in setup.sh
# https://knowledge.udacity.com/questions/533049

TEST_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.environ.get('PRODUCER_TOKEN')

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone project test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        # https://knowledge.udacity.com/questions/373159
        # read again  - might be useful?
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DATABASE_URI)
        self.casting_assistant = ASSISTANT_TOKEN
        self.casting_director = DIRECTOR_TOKEN
        self.executive_producer = PRODUCER_TOKEN

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    #Ref: https://knowledge.udacity.com/questions/294099
    # helper function that produces a header in the correct format

    # https://knowledge.udacity.com/questions/492044
    # if issues with self. being passed
    def get_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    # ----------------------------------------------------------------------------#
    # Actor Tests
    # ----------------------------------------------------------------------------#

    # Ref: https://knowledge.udacity.com/questions/972850
    def test_get_actors(self):
        """ Test successful behaviour of GET /actors endpoint

        The test_get_actors test uses the GET method and the correct
        authorisation to get all the avaliable actors from the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - that "actors" contains values.
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_401(self):
        """ Test 401 error behaviour for GET /actors endpoint

        The test_get_actors_401 test tries to call the endpoint without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """

        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_get_actors_405(self):
        """ Test 405 error behaviour for GET /actors endpoint

        The test_get_actors_405 test uses the incorrect
        POST method to validate that the expected HTTP exception is
        raised if the incorrect method is used to query the endpoint.

        The assert statements check that the endpoint returns:
        - a status code of 405
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "The method is not allowed for the requested URL.".
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().post("/actors", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The method is not allowed for the requested URL.")

    #TODO: review this - is it too broad?
    def test_get_actor_movies(self):
        """ Test of successful behaviour of GET /actor/actor_id/movies endpoint
        
        The test_get_actor_movies test uses the GET method and the correct
        authorisation to list the movies an actor is cast in based on the
        actor_id.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, 
            - that "actor" contains values, and
            - that "movies cast in" contains values, either a list of movies
                or a message stating that the actor has not been cast yet
        """
        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/actor/" + str(VALID_ACTOR_ID)+ "/movies", headers=auth_header)

        #TODO - make this it's own method?
        actor = Actor.query.filter(
                Actor.id == VALID_ACTOR_ID
                ).one_or_none()

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"], actor.name)
        self.assertTrue(len(data["movies cast in"]))

    def test_get_actor_movies_404(self):
        """ Test of 404 error behaviour of GET /actor/actor_id/movies endpoint
        
        The test_get_actor_movies_404 test uses the GET method and the correct
        authorisation to pass an invalid actor_id.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No actor with id "+ str(INVALID_ACTOR_ID) +" exists"
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/actor/" + str(INVALID_ACTOR_ID)+ "/movies", headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No actor with id "+ str(INVALID_ACTOR_ID) +" exists")

    def test_add_actor(self):
        """ The test_add_new_actor test uses the POST method to
        add a new actor to the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "created" value.
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/actors/add",
            json=VALID_ACTOR,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_add_actor_422(self):
        """ The test_add_actor_422 test uses a 
        missing field to validate that the expected HTTP exception
        is raised if incorrect json data is passed to the endpiont.

        The assert statements check that the endpoint returns:
        - a status code of 422
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "The request was well-formed but was unable to be followed due to semantic errors.".
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/actors/add",
            json=INVALID_ACTOR,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],
                         "The request was well-formed but was unable to be followed due to semantic errors.")

    def test_add_actor_401(self):
        """ Test 401 error behaviour for POST /actors/add endpoint

        The test_add_actor_401 test tries to add an actor without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """

        res = self.client().post("/actors/add",
            json=VALID_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_add_actor_403(self):
        """ Test 403 error behaviour for POST /actors/add endpoint

        The test_add_movie_403 test tries to add an actor without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().post(
            "/actors/add",
            json=VALID_ACTOR,
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_edit_actor(self):
        """ Test successful behaviour for PATCH /actors/actor_id/edit endpoint
        
        The test_edit_actor test uses the PATCH method to
        edit an actor in the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "actor" value.
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().patch(
            "/actors/" + str(VALID_ACTOR_ID)+ "/edit",
            json=VALID_ACTOR_PATCH,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_edit_actor_404(self):
        """ Test 404 error behaviour for PATCH /actors/actor_id/edit endpoint
        
        The test_edit_actor_404 test uses a 
        invalid actor_id to validate that the expected HTTP exception
        is raised if incorrect json data is passed to the endpiont.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No actor with id "+ str(INVALID_ACTOR_ID) +" exists".
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().patch(
            "/actors/" + str(INVALID_ACTOR_ID)+ "/edit",
            json=VALID_ACTOR_PATCH,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No actor with id "+ str(INVALID_ACTOR_ID) +" exists")
    
    def test_edit_actor_401(self):
        """ Test 401 error behaviour for PATCH /actors/actor_id/edit endpoint

        The test_edit_actor_401 test tries to edit an actor without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """
        res = self.client().patch(
            "/actors/" + str(VALID_ACTOR_ID)+ "/edit",
            json=VALID_ACTOR_PATCH)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_edit_actor_403(self):
        """ Test 403 error behaviour for PATCH /actors/actor_id/edit endpoint

        The test_edit_movie_403 test tries to edit an actor without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().patch(
            "/actors/" + str(VALID_ACTOR_ID)+ "/edit",
            json=VALID_ACTOR_PATCH,
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")
    
    def test_delete_actor(self):
        """ Test successful behaviour for DELETE /actors/actor_id/delete endpoint
        
        The test_delete_actor test uses the DELETE method to
        delete an actor from the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "deleted" value matching the id in the endpoint.
        """
        # Add an actor to the database
        auth_header = self.get_headers(self.casting_director)
        add_actor = self.client().post(
            "/actors/add",
            json=VALID_ACTOR,
            headers=auth_header)
        
        # get the new actors id
        actor_data = json.loads(add_actor.data)
        actor_id = actor_data["created"]["id"]

        # Try to delete the actor
        auth_header = self.get_headers(self.casting_director)
        res = self.client().delete("/actors/" + str(actor_id)+ "/delete",
            headers=auth_header)
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], actor_id)

    def test_delete_actor_404(self):
        """ Test 404 error behaviour for DELETE /actors/actor_id/delete endpoint
         
        The test_delete_actor_404 test validates
        that the expected HTTP exception is raised if the deletion of
        a actor that does not exist in the database is attempted.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No actor with id "+ str(INVALID_ACTOR_ID) +" exists".
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().delete("/actors/" + str(INVALID_ACTOR_ID)+ "/delete",
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No actor with id "+ str(INVALID_ACTOR_ID) +" exists")
    
    def test_delete_actor_401(self):
        """ Test 401 error behaviour for DELETE /actors/actor_id/delete endpoint

        The test_delete_actor_401 test tries to delete an actor without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """
        # Add an actor to the database
        auth_header = self.get_headers(self.casting_director)
        add_actor = self.client().post(
            "/actors/add",
            json=VALID_ACTOR,
            headers=auth_header)
        
        # get the new actors id
        actor_data = json.loads(add_actor.data)
        actor_id = actor_data["created"]["id"]

        # Try to delete the actor
        res = self.client().delete("/actors/" + str(actor_id)+ "/delete")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_delete_actor_403(self):
        """ Test 403 error behaviour for DELETE /actors/actor_id/delete endpoint

        The test_delete_movie_403 test tries to delete an movie without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """
        # Add an actor to the database
        auth_header = self.get_headers(self.casting_director)
        add_actor = self.client().post(
            "/actors/add",
            json=VALID_ACTOR,
            headers=auth_header)
        
        # get the new actors id
        actor_data = json.loads(add_actor.data)
        actor_id = actor_data["created"]["id"]

        # Try to delete the actor
        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().delete("/actors/" + str(actor_id)+ "/delete",
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")
    # ----------------------------------------------------------------------------#
    # Movie Tests
    # ----------------------------------------------------------------------------#

    def test_get_movies(self):
        """ Test successful behaviour of GET /movies endpoint
        
        The test_get_moviess test uses the GET method and the correct
        authorisation to get all the avaliable movies from the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - that "movies" contains values.
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/movies", headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_movies_401(self):
        """ Test 401 error behaviour for GET /movies endpoint

        The test_get_movies_401 test tries to call the endpoint without the
        required authorization header to validate that the expected HTTP exception is
        raised if the incorrect method is used to query the endpoint.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """

        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_get_movies_405(self):
        """ Test 405 error behaviour for GET /movies endpoint

        The test_get_movies_405 test uses the incorrect
        POST method to validate that the expected HTTP exception is
        raised if the incorrect method is used to query the endpoint.

        The assert statements check that the endpoint returns:
        - a status code of 405
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "The method is not allowed for the requested URL.".
        """
        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().post("/movies", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The method is not allowed for the requested URL.")

    #TODO: review this - is it too broad?
    def test_get_movie_actors(self):
        """ Test successful behaviour of GET /movie/movie_id/actors endpoint
        
        The test_get_movie_actors test uses the GET method and the correct
        authorisation to list the actors cast in a movie based on the
        movie_id.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, 
            - that "movie" contains values, and
            - that "actors" contains values, either a list of movies
                or a message stating that the actor has not been cast yet
        """
        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/movie/" + str(VALID_MOVIE_ID)+ "/actors", headers=auth_header)

        #TODO - make this it's own method?
        movie = Movie.query.filter(
                Movie.id == VALID_MOVIE_ID
                ).one_or_none()

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"], movie.title)
        self.assertTrue(len(data["actors cast"]))

    def test_get_movie_actors_404(self):
        """ Test 404 error behaviour of GET /movie/movie_id/actors endpoint
        
        The test_get_movie_actors_404 test uses the GET method and the correct
        authorisation to pass an invalid movie_id.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No movie with id "+ str(INVALID_MOVIE_ID) +" exists".
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().get("/movie/" + str(INVALID_MOVIE_ID)+ "/actors", headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No movie with id "+ str(INVALID_MOVIE_ID) +" exists")

    def test_add_movie(self):
        """ The test_add_movie test uses the POST method to
        add a new movie to the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "created" value.
        """
        auth_header = self.get_headers(self.executive_producer)
        res = self.client().post(
            "/movies/add",
            json=VALID_MOVIE,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_add_movie_422(self):
        """ The test_add_movie_422 test uses a 
        missing field other then genre to validate that the expected 
        HTTP exception is raised if incorrect json data is passed to
        the endpoint.

        The assert statements check that the endpoint returns:
        - a status code of 422
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "The request was well-formed but was unable to be followed due to semantic errors.".
        """
        auth_header = self.get_headers(self.executive_producer)
        res = self.client().post(
            "/movies/add",
            json=INVALID_MOVIE,
            headers=auth_header)
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],
                         "The request was well-formed but was unable to be followed due to semantic errors.")
        
    def test_add_movie_401(self):
        """ Test 401 error behaviour for POST /movies/add endpoint

        The test_add_movie_401 test tries to add an movie without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """

        res = self.client().post("/movies/add",
            json=VALID_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_add_movie_403(self):
        """ Test 403 error behaviour for POST /movies/add endpoint

        The test_add_movie_403 test tries to add an movie without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """

        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/movies/add",
            json=VALID_MOVIE,
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_edit_movie(self):
        """ Test successful behaviour for PATCH /movies/movie_id/edit endpoint
        
        The test_edit_movie test uses the PATCH method to
        edit a movie in the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "movie" value.
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().patch(
            "/movies/" + str(VALID_MOVIE_ID)+ "/edit",
            json=VALID_MOVIE_PATCH,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_edit_movie_404(self):
        """ Test 404 error behaviour for PATCH /movies/movie_id/edit endpoint
        
        The test_edit_movie_404 test uses a 
        invalid movie_id to validate that the expected HTTP exception
        is raised if incorrect json data is passed to the endpiont.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No movie with id "+ str(INVALID_MOVIE_ID) +" exists".
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().patch(
            "/movies/" + str(INVALID_MOVIE_ID)+ "/edit",
            json=VALID_MOVIE_PATCH,
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No movie with id "+ str(INVALID_MOVIE_ID) +" exists")

    def test_edit_movie_401(self):
        """ Test 401 error behaviour for PATCH /movies/movie_id/edit endpoint

        The test_edit_movie_401 test tries to edit an movie without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """
        res = self.client().patch(
            "/movies/" + str(VALID_MOVIE_ID)+ "/edit",
            json=VALID_MOVIE_PATCH)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_edit_movie_403(self):
        """ Test 403 error behaviour for PATCH /movies/movie_id/edit endpoint

        The test_edit_movie_403 test tries to edit an movie without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """

        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().patch(
            "/movies/" + str(VALID_MOVIE_ID)+ "/edit",
            json=VALID_MOVIE_PATCH,
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_delete_movie(self):
        """ Test successful behaviour for DELETE /movies/movie_id/delete
        
        The test_delete_movie test uses the DELETE method to
        delete an movie from the test database.

        The assert statements check that the endpoint returns:
        - a status code of 200
        - a json object with: 
            - a "success" value of True, and
            - a "deleted" value matching the id in the endpoint.
        """
        # Add a movie to the database
        auth_header = self.get_headers(self.executive_producer)
        add_movie = self.client().post(
            "/movies/add",
            json=VALID_MOVIE,
            headers=auth_header
            )

        # get the new movies id
        movie_data = json.loads(add_movie.data)
        movie_id = movie_data["created"]["id"]
        
        # Attempt to delete movie
        auth_header = self.get_headers(self.executive_producer)
        res = self.client().delete("/movies/" + str(movie_id) + "/delete", headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], movie_id)

    def test_delete_movie_404(self):
        """ Test 404 error behaviour for DELETE /movies/movie_id/delete
        
        The test_delete_movie_404 test validates
        that the expected HTTP exception is raised if the deletion of
        a movie that does not exist in the database is attempted.

        The assert statements check that the endpoint returns:
        - a status code of 404
        - a json object with: 
            - a "success" value of False, and
            - a "message" of "No movie with id "+ str(INVALID_MOVIE_ID) +" exists".
        """
        
        auth_header = self.get_headers(self.executive_producer)
        res = self.client().delete("/movies/" + str(INVALID_MOVIE_ID) + "/delete", headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No movie with id "+ str(INVALID_MOVIE_ID) +" exists")

    def test_delete_movie_401(self):
        """ Test 401 error behaviour for DELETE /actors/actor_id/delete

        The test_delete_movie_401 test tries to delete an movie without the
        required authorization header to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """
        # Add a movie to the database
        auth_header = self.get_headers(self.executive_producer)
        add_movie = self.client().post(
            "/movies/add",
            json=VALID_MOVIE,
            headers=auth_header
            )

        # get the new movies id
        movie_data = json.loads(add_movie.data)
        movie_id = movie_data["created"]["id"]
        
        # Attempt to delete movie
        res = self.client().delete("/movies/" + str(movie_id) + "/delete")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_delete_movie_403(self):
        """ Test 403 error behaviour for DELETE /movies/movie_id/delete

        The test_delete_movie_403 test tries to delete an movie without the
        required permission to validate that the expected HTTP exception is
        raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """
       # Add a movie to the database
        auth_header = self.get_headers(self.executive_producer)
        add_movie = self.client().post(
            "/movies/add",
            json=VALID_MOVIE,
            headers=auth_header
            )

        # get the new movies id
        movie_data = json.loads(add_movie.data)
        movie_id = movie_data["created"]["id"]
        
        # Attempt to delete movie
        auth_header = self.get_headers(self.casting_director)
        res = self.client().delete("/movies/" + str(movie_id) + "/delete",headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_cast_actors_in_movies(self):
        """ Test of successful behaviour of the POST /movie/movie_id/actor/actor_id

        The assert statements check that the endpoint returns:
        - 
        """

        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/movie/" + str(VALID_MOVIE_ID) + "/actor/" + str(VALID_ACTOR_ID),
            headers=auth_header)

        data = json.loads(res.data)

        #TODO - make this it's own method?
        movie = Movie.query.filter(
                Movie.id == VALID_MOVIE_ID
                ).one_or_none()

        actor = Actor.query.filter(
                Actor.id == VALID_ACTOR_ID
                ).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["movie"], movie.title)
        self.assertEqual(data["actor cast"], actor.name)

    def test_cast_actors_in_movies_404_movie_not_found(self):
        """ Test of 404 error behaviour of the 
        POST /movie/movie_id/actor/actor_id endpoint when the movie_id 
        is invalid

        The assert statements check that the endpoint returns:
        - 
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/movie/" + str(INVALID_MOVIE_ID) + "/actor/" + str(VALID_ACTOR_ID),
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No movie with id "+ str(INVALID_MOVIE_ID) +" exists")

    def test_cast_actors_in_movies_404_actor_not_found(self):
        """ Test of 404 error behaviour of the 
        POST /movie/movie_id/actor/actor_id endpoint when the actor_id 
        is invalid

        The assert statements check that the endpoint returns:
        - 
        """
        auth_header = self.get_headers(self.casting_director)
        res = self.client().post(
            "/movie/" + str(VALID_MOVIE_ID) + "/actor/" + str(INVALID_ACTOR_ID),
            headers=auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No actor with id "+ str(INVALID_ACTOR_ID) +" exists")
    
    def test_cast_actors_in_movies_401(self):
        """ Test 401 error behaviour for POST /movie/movie_id/actor/actor_id

        The test_cast_actors_in_movies_401 test tries to cast an actor in a 
        movie without the required authorization header to validate that the
        expected HTTP exception is raised.

        The assert statements check that the endpoint returns:
        - a status code of 401
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "authorization_header_missing".
        """

        res = self.client().post(
            "/movie/" + str(VALID_MOVIE_ID) + "/actor/" + str(VALID_ACTOR_ID))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_cast_actors_in_movies_403(self):
        """ Test 403 error behaviour for POST /movie/movie_id/actor/actor_id

        The test_cast_actors_in_movies_403 test tries to cast an actor in a 
        movie without the required permission to validate that the expected 
        HTTP exception is raised.

        The assert statements check that the endpoint returns:
        - a status code of 403
        - a json object with: 
            - a "success" value of False, and
            - a "code" value of "unauthorized".
        """
        auth_header = self.get_headers(self.casting_assistant)
        res = self.client().post(
            "/movie/" + str(VALID_MOVIE_ID) + "/actor/" + str(VALID_ACTOR_ID),
            headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)
