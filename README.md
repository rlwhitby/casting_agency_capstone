# casting_agency_capstone
## Overview
> This is my final capstone project for the Udacity Full Stack Web Developer Nanodegree.

> It is a demonstration project to showcase my skills in Flask, SQLAlchemy, Auth0, Render to develop and deploy an API backend application.
> 
> This application follows [PEP8 style guidelines](https://peps.python.org/pep-0008/). Pycodestyle is installed to check the python code files against the PEP8 style conventions.

# Deployment
This application is hosted on [Render](https://render.com/) at: #TODO

## Main Files: Project Structure

  ```sh
├── application
│   ├── __init__.py
│   ├── auth
│   │   └── auth.py *** authorisation methods and error handling
│   ├── errors
│   │   ├── __init__.py
│   │   └── handlers.py *** error handling
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py *** main API routes
│   └── models
│       ├── enums.py
│       └── models.py *** database models
├── app.py *** the main driver of the app
├── capstone.psql
├── config.py *** contains the configurations of the Development, Test and Production environments
├── README.md
├── requirements.txt *** the dependencies for the application
├── setup.sh *** script file to set environment variables
├── test_app.py *** application unit tests
└── testing_constants.py

```

# Local Development
This section describes how to set up the local development environment and run the project locally.

## Install Dependancies
1. **Python 3.11** - Follow the instructions to install the latest version of python in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **PostgreSQL 14.12** Follow the instructions to install [PostgreSQL](https://www.postgresql.org/).
The database URL in `setup.sh` has the username and password `postgres:postgres`. If you have a different username and password, update the `DATABASE_URL` and `TEST_DATABASE_URL` in `setup.sh`.

3. **Virtual Environment** - The built-in Python3 module `venv` is used to create an isolated Python environment.
If you want to use a different tool, instructions for setting up a different virtual environment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

If using `venv`, run the following commands to create and activate a new environment.
```bash
# create virtual env
python3 -m venv venv

# activate it 
source venv/bin/activate
```

4. **PIP Dependencies** - Once you have your virtual environment setup and running, install the required packages by running:
```bash
pip install -r requirements.txt
```

5. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework handling requests and responses for the application.

 - [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) are libraries to handle the PostgreSQL database.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Auth0](https://auth0.com/) is a platform that provides authentication and authorization for web, mobile, and legacy applications.


## Setup environment variables
Export the required environment variables by running:
```bash
source setup.sh
```

## Setup the database
With PostgreSQL running, login and create a `capstone` database.
```bash
# login to postgres
sudo -u postgres -i

# drop the capstone database, if one already exists
dropdb capstone

# create the capstone database
createdb capstone
exit
```

Populate the database from the provided `capstone.psql` file.

```bash
sudo -u postgres psql -d capstone < capstone.psql
```


## Run the Application
The application is hosted at the default `http://127.0.0.1:5000/` when running locally.

This command runs the app in [debug mode](https://flask.palletsprojects.com/en/3.0.x/config/) - an interactive debugger is shown in the console and restarts the server whenever changes are made.

Run the following command to start the application locally:
```bash
flask --app app --debug run
```

## Testing

The [unittest](https://docs.python.org/3/library/unittest.html) framework is used in this application to run the tests.

To setup the testing database, login and create a `capstone_test` database.
```bash
# login to postgres
sudo -u postgres -i

# drop the capstone_test database, if one already exists
dropdb capstone_test

# create the capstone_test database
createdb capstone_test
exit
```
The `capstone_test` database does not need to be pre-populated with data.

### Running Tests

Use the following command to run the tests:
```bash
python test_app.py

# to run individual tests
python test_app.py CapstoneTestCase.test_name
# example
python test_app.py CapstoneTestCase.test_delete_movie_403
```


# API Reference
## API Authentication
All of the endpoints, except the index and /authorization/url routes, require permissions passed by a Bearer token.

Use the following url or the `/authorization/url` when the application is running locally, and the login details of the roles,to create new JWT tokens, if the tokens saved in the `setup.sh` and the `postman collection` files have expired:

`https://dev-dudattxg70vfdgkq.au.auth0.com/authorize?audience=castingAgencyAPI&response_type=token&client_id=t4oSkhZhgtTiA9Tcy1eR6eEYiF88QtXg&redirect_uri=http://127.0.0.1:8080/login-results`

There are three roles for the application:
- Casting Assistant
    - Can view the details of actors and movies
    - Permissions:
        - `view:actors`
        - `view:movies`
    - Login Details (if a new token is required):
        - `casting_assistant@gmail.com`
        - `passwordAssistant3456#`


    <details>
    <summary>Casting Assistant Token:</summary>
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWU1MGJlNzQ5YWZhYWEyOWI2NWIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxNDUyMDY0LCJleHAiOjE3MjE1Mzg0NjQsInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.KZaflK4gZ26vV_u02nVbF87wwL2iGSyqmZEyjoXq4nPqAmaZdnUQhPTANAuwu4yQL7xyIbFkzYp2BZgjvYBu4Qq7mBg5z9JdK3bd4350bRzS_g5Vlll2jgZmx9YOmqBnFeD7dOTGXCVaJ97B_b6GD8sHRyutSy9hKUuir43VNEU-I3pvGemSEm8Mo9zB4Gk7fA6f2N54pybVyt2JY2VyjPtDMm2UC5BP5v85sZVl6L08mTWrHCptx2R8adQolua5nt1l1I3-lUgQwpMRN-Ixq8gomKrq0ys32SKKDwDRrBUhtKDmGEBMgTTtbnPL8QUoXfQOgH-YDdyzfisek_wrbg
    </details>


- Casting Director
    - Same permissions as the Casting Assistant,
    - Can add or delete actors,
    - Can edit actors and movies, and
    - Can cast actors in movies
    - Permissions:
        - `view:actors`
        - `view:movies`
        - `post:actors`
        - `update:actors`
        - `delete:actors`
        - `update:movies`
        - `post:cast_actors`
    - Login Details (if a new token is required):
        - `casting_director@gmail.com`
        - `passwordDirector8756@`


    <details>
    <summary>Casting Director Token:</summary>
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWY1NDA5MGYyMzM0YjczY2MxZmQiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxNDUyMjI4LCJleHAiOjE3MjE1Mzg2MjgsInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwicG9zdDphY3RvcnMiLCJwb3N0OmNhc3RfYWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.qNGc0RXFGPZs4a3gh-WJ02jtcI3py-BxH9-VWZklRhQyePtNszBvzTqTy4db8BG4qt6J2hR9hxtCeCpJBny2XXKsuYtGdVtKd5Y_4R4p0QAnQmSpaHo94V02zwvy6hXGlUEwCxMrLmPNyvHANdvYqh9z9C353lWZadV5LCpDCc-jjEyChLp7xynG9IRePLUiwm3ILsLU3waGuFXN_KDa_hHYDfY1mRFU4ZRqa2KFkfy0Mmuy7D9j042LSAnG04KSobu6AQ_nbWpXJ9fcVQ4dpysrlqmwPengc-offjsvsSOzbYMYx3OUxYdmAIQMblARqWsXsOCN_O1xOxl8fIurTA
    </details>


- Executive Producer
    - Same permissions as the Casting Director, and
    - Can add or delete movies
    - Permissions:
        - `view:actors`
        - `view:movies`
        - `post:actors`
        - `update:actors`
        - `delete:actors`
        - `update:movies`
        - `post:cast_actors`
        - `post:movies`
        - `delete:movies`
    - Login Details (if a new token is required):
        - `executive_producer@gmail.com`
        - `passwordProducer4704$`


    <details>
    <summary>Executive Producer Token:</summary>
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWY5NTg4ZjJlODZhZjRmOWVlZmYiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxNDUyMzE3LCJleHAiOjE3MjE1Mzg3MTcsInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0X2FjdG9ycyIsInBvc3Q6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.P5C5u0SlInqMDY_a84rQ1vISj0OYZNYboK76BYmVdYayZ2MtZ2J2VLIMwhq37lPUZs6GrZ3aO3frPKgNZzV2S_yaNMX6YDtN1NrqEhJSMxutt1n6m8ozL0E9wNnehFMTF2xAVFG5H9KJYG2wdxkIUp9Tiym4DjSlYzOgYSJ16B6hhufqPxvCiggMf8XkGrQblHAz72_y5eX3Xu87oep9rXdj5SAQ9FGlxX4FE0QZhbqLyWS3l93kTIc5FXSoTIJobrtAONCHjiwmYX6UU7l6DQEY77d3e37TolKRCPkhFlwOw-cbRB8iuK1LmdBy-2Ri8HtamXy6Dr91jfRIyQCuIA
    </details>

## API Testing
[Postman](https://getpostman.com) can be used to test the application endpoints.

> Import the postman collections
>
> Local server: `./casting_agency_local.postman_collection.json`
>
> Production Server: `./casting_agency_production.postman_collection.json`
> 
> If the tokens provided have expired, new tokens can be added by right-clicking the collection folder for Casting Assistant, Casting Director and Executive Producer, navigating to the authorization tab, and pasting the token for each role in the token field.
>
> Run the collection.

## Error Handling
Errors are returned as JSON objects in the following format:

```json
{
    "error": "400 Bad Request",
    "message": "Failed to decode JSON object: Expecting value: line 1 column 10 (char 9)",
    "success": false
}
```

### Error types

The API will return one of seven error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error

## Endpoints
### GET /
General:
- Returns a welcome message.
- Public endpoint, no authentication required. 
- Request Arguments: none.
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/`

<details>
<summary>Sample Response:</summary>

```json
{
    "message": "Welcome to the Casting Agency App!"
}
```
</details>

### GET /authorization/url
General:
- A helper function that returns the authorization login url for generating new JWT tokens.
- Public endpoint, no authentication required. 
- Request Arguments: none.
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/authorization/url`

<details>
<summary>Sample Response:</summary>

```json
{
    "url": "https://dev-dudattxg70vfdgkq.au.auth0.com/authorize?audience=castingAgencyAPI&response_type=token&client_id=t4oSkhZhgtTiA9Tcy1eR6eEYiF88QtXg&redirect_uri=http://127.0.0.1:8080/login-results"
}
```
</details>

## Actor Endpoints
### GET /actors
General:
- Returns a success value and a list of actors.
- Private endpoint, requires `view:actors` permission.
- Request Arguments: a decoded JWT token payload.
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/actors`

<details>
<summary>Sample Response:</summary>

```json
{
    "actors": [
        {
            "age": 52,
            "gender": "Male",
            "id": 1,
            "movies": "This actor has been cast in 2 movies",
            "name": "Ke Huy Quan"
        },
        {
            "age": 81,
            "gender": "Male",
            "id": 2,
            "movies": "This actor has been cast in 1 movie",
            "name": "Harrison Ford"
        },
        {
            "age": 33,
            "gender": "Female",
            "id": 3,
            "movies": "This actor has not been cast in any movies",
            "name": "Jennifer Lawrence"
        }
    ],
    "success": true
}
```
</details>

### GET /actor/{actor_id}/movies
General:
- Returns a success value, the actor's name and a list of movies the actor has been cast in.
- Private endpoint, requires the `view:actors` permission.
- Request Arguments: a decoded JWT token payload and the actor id.
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/actor/1/movies`

<details>
<summary>Sample Response:</summary>

```json
{
    "actor": "Ke Huy Quan",
    "movies cast in": [
        {
            "actors": "This movie has 2 actors",
            "genre": "Adventure",
            "id": 1,
            "release date": "Tue, 08 May 1984 00:00:00 GMT",
            "title": "Indiana Jones and the Temple of Doom"
        },
        {
            "actors": "This movie has 1 actor",
            "genre": "Action",
            "id": 2,
            "release date": "Fri, 11 Mar 2022 00:00:00 GMT",
            "title": "Everything Everywhere All at Once"
        }
    ],
    "success": true
}
```
</details>

### POST /actors/add 
General:
- Creates a new actor using the submitted name, age and gender.
- Private endpoint, requires the `post:actors` permission.
- Request Arguments: a decoded JWT token payload.
- Request Body:
    - name: string, required.
    - age: integer, required.
    - gender: string, optional.

Sample Request:

`curl -d '{"name": "Ke Huy Quan", "age": 52, "gender": "Male"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/actors/add`

<details>
<summary>Sample Response:</summary>

```json
{
  "created": {
    "age": 52,
    "gender": "Male",
    "id": 1,
    "movies": "This actor has not been cast in any movies",
    "name": "Ke Huy Quan"
  },
  "success": true
}
```
</details>

### PATCH /actors/{actor_id}/edit
General:
- Edits the information for a chosen actor using the submitted name, age and gender.
- Private endpoint, requires the `update:actors` permission.
- Request Arguments: a decoded JWT token payload and actor_id (int).
- Request Body:
    - name: string, optional.
    - age: integer, optional.
    - gender: string, optional.

Sample Request:

`curl -d '{"name": "Jane Doe edit", "age": 23, "gender": "Female"}' -H "Content-Type: application/json" -X PATCH http://127.0.0.1:5000/actors/2/edit`

<details>
<summary>Sample Response:</summary>

```json
{
  "actor": {
    "age": 23,
    "gender": "Female",
    "id": 2,
    "movies": "This actor has been cast in 1 movie",
    "name": "Jane Doe edit"
  },
  "success": true
}
```
</details>

### DELETE /actors/{actor_id}/delete
General:
- Deletes the actor of the given actor_id if it exists. 
- Private endpoint, requires the `delete:actors` permission.
- Request Arguments: a decoded JWT token payload and actor_id (int).
- Request Body: none.

Sample Request:

`curl -X DELETE http://127.0.0.1:5000/actors/1/delete`

<details>
<summary>Sample Response:</summary>

```json
{
    "success": true,
    "deleted id": 1,
}
```
</details>


## Movie Endpoints
### GET /movies
General:
- Returns a success value and a list of movie objects.
- Private endpoint, requires `view:movies` permission.
- Request Arguments: a decoded JWT token payload.
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/movies`

<details>
<summary>Sample Response:</summary>

```json
{
    "movies": [
        {
            "actors": "This movie has 2 actors",
            "genre": "Adventure",
            "id": 1,
            "release date": "Tue, 08 May 1984 00:00:00 GMT",
            "title": "Indiana Jones and the Temple of Doom"
        },
        {
            "actors": "This movie has 1 actor",
            "genre": "Action",
            "id": 2,
            "release date": "Fri, 11 Mar 2022 00:00:00 GMT",
            "title": "Everything Everywhere All at Once"
        },
        {
            "actors": "This movie has no actors",
            "genre": "Action",
            "id": 3,
            "release date": "Mon, 12 Mar 2012 00:00:00 GMT",
            "title": "The Hunger Games"
        }
    ],
    "success": true
}
```
</details>

### GET /movie/{movie_id}/actors
General:
- Returns a success value, the movie title and a list of actors cast in the movie.
- Private endpont, requires the `view:movies` permission.
- Request Arguments: a decoded JWT token payload and the movie id (int).
- Request Body: none.

Sample Request:

`curl http://127.0.0.1:5000/movie/1/actors`

<details>
<summary>Sample Response:</summary>

```json
{
    "actors cast": [
        {
            "age": 52,
            "gender": "Male",
            "id": 1,
            "movies": "This actor has been cast in 2 movies",
            "name": "Ke Huy Quan"
        },
        {
            "age": 81,
            "gender": "Male",
            "id": 2,
            "movies": "This actor has been cast in 1 movie",
            "name": "Harrison Ford"
        }
    ],
    "movie": "Indiana Jones and the Temple of Doom",
    "success": true
}
```
</details>

### POST /movies/add 
General:
- Creates a new movie using the submitted title, release date and genre.
- Private endpont, requires the `post:movies` permission.
- Request Arguments: a decoded JWT token payload.
- Request Body:
    - title: string, required.
    - release_date: date a valid date format e.g. "mm-dd-YYYY", required.
    - genre: string, must match an option in the GenreEnum list, required.

#### GenreEnum List
> Action, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Musical, Romance, Scifi

Sample Request:

`curl -d '{"title": "Indiana Jones and the Temple of Doom", "release_date": "08-05-1984", "genre": "Adventure"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/movies/add`

<details>
<summary>Sample Response:</summary>

```json
{
  "created": {
    "actors": "This movie has no actors",
    "genre": "Adventure",
    "id": 1,
    "release date": "Sun, 05 Aug 1984 00:00:00 GMT",
    "title": "Indiana Jones and the Temple of Doom"
  },
  "success": true
}
```
</details>


### PATCH /movies/{movie_id}/edit
General:
- Edits the selected movie using the submitted title, release date and/or genre.
- Private endpont, requires the `update:movies` permission.
- Request Arguments: a decoded JWT token payload and movie_id (int).
- Request Body:
    - title: string, optional.
    - release_date: date a valid date format e.g. "mm-dd-YYYY", optional.
    - genre: string, must match an option in the GenreEnum list, optional.

#### GenreEnum List
> Action, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Musical, Romance, Scifi

Sample Request:

`curl -d '{"title": "Indiana Jones and the Temple of Doom", "release_date": "05-08-1984"}' -H "Content-Type: application/json" -X PATCH http://127.0.0.1:5000/movies/1/edit`

<details>
<summary>Sample Response:</summary>

```json
{
  "movie": {
    "actors": "This movie has no actors",
    "genre": "Adventure",
    "id": 1,
    "release date": "Tue, 08 May 1984 00:00:00 GMT",
    "title": "Indiana Jones and the Temple of Doom"
  },
  "success": true
}
```
</details>

### DELETE /movies/{movie_id}/delete
General:
- Deletes the movie of the given movie_id if it exists. 
- Private endpoint, requires the `delete:movies` permission.
- Request Arguments: a decoded JWT token payload and movie_id (int).
- Request Body: none.

Sample Request:

`curl -X DELETE http://127.0.0.1:5000/movies/1/delete`

<details>
<summary>Sample Response:</summary>

```json
{
    "success": true,
    "deleted id": 1,
}
```
</details>

### POST /movie/{movie_id}/actor/{actor_id}
General:
- Casts an actor in a movie if the given actor_id and movie_id both exist. 
- Private endpoint, requires the `post:cast_actors` permission.
- Request Arguments: a decoded JWT token payload, actor_id (int) and movie_id (int).
- Request Body: none.

Sample Request:

`curl -X POST http://127.0.0.1:5000/movie/3/actor/3`

<details>
<summary>Sample Response:</summary>

```json
{
    "actor cast": "Jennifer Lawrence",
    "movie": "The Hunger Games",
    "success": true
}
```

</details>

# Acknowledgements
[Udacity](https://learn.udacity.com/) for the Casting Agency Specifications and the Full Stack Web Developer Nanodegree course.