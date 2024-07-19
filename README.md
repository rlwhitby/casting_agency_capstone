# casting_agency_capstone
Final capstone for FSND 

# casting_agency Application

## Introduction

## Overview

## Tech Stack (Dependencies)
#TODO: rewrite
### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```


> Description of project and motivation
> 
> Screenshots (if applicable), with captions
> 
> This application follows [PEP8 style guidelnes](https://peps.python.org/pep-0008/). Pycodestyle is installed to check the python code file against the PEP8 style conventions.
> 
> `# noqa` is used at the end of some comments to ignore the pycodestyle check for E501: line to long.


## Main Files: Project Structure

  ```sh
├── application
│   ├── extensions.py
│   ├── __init__.py
│   ├── auth
│   │   └── auth.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   └── models
│       ├── enums.py
│       └── models.py
├── app.py *** the main driver of the app
├── capstone.psql
├── config.py ***
├── README.md
├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
├── setup.sh
├── test_app.py
└── test_constants.py

```




# Getting Started
## Prerequisites & Local Development, including how to set up the local development environment and run the project locally

# Local Development
## Install Dependancies
### Python 3.11

### virtual environment
```bash
#TODO swap to venv instructions

conda activate casting_agency_env

# create virtual env
python3 -m venv venv

# activate it 
source venv/bin/activate
```

### Postgresql

### Install requirements
```bash
pip install -r requirements.txt
```

## Setup environment variables
```bash
source setup.sh
```

## Setup database
```bash
sudo -u postgres -i
dropdb capstone
createdb capstone
exit
```
## go to Run app section if you want a blank database

## if you want to seed the database with initial data:

```bash

sudo -u postgres psql -d capstone < capstone.psql

sudo -u postgres psql capstone
\dt
SELECT * FROM actors;
\q


```

## Run app
This command runs the app in developement mode - shows an interactive debugger in the console and restarts the server whenever changes are made - [Debug Mode](https://flask.palletsprojects.com/en/3.0.x/config/)
```bash
flask --app app --debug run

#TODO: flask run if set from environment varibles?
```

## Tests and how to run them

**Running Tests**
```bash
sudo -u postgres -i
dropdb capstone_test
createdb capstone_test
exit

#TODO: this might not be needed?
sudo -u postgres psql -d capstone_test < capstone.psql
python test_app.py

# to run individual tests
python test_app.py CapstoneTestCase.test_name
# example
python test_app.py CapstoneTestCase.test_delete_movie_403
```

python -m coverage run -m unittest
python -m coverage report
python -m coverage report --skip-covered 
python -m coverage html

 https://stackoverflow.com/questions/68004558/see-html-preview-on-side-tab-in-vscode

# API Reference

# API Documentation

## Introduction
## Getting Started
### Base URL
Host URL
Local deployment - the application is hosted at the default, ``http://127.0.0.1:5000/``
### API Keys /Authentication (if applicable)

Casting Assistant

casting_assistant@gmail.com
passwordAssistant3456#

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWU1MGJlNzQ5YWZhYWEyOWI2NWIiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxMzgwNzgwLCJleHAiOjE3MjE0NjcxODAsInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.eLTgF0FuQMlsgUxbJRba4QbR4JEdpS2msutuZzvRYfeI9qBXvWr4YTGI1sLe5HK2h1sil_A6-1JH8AmimK-JVYzDsryldq7SRlTtreNUSj4oA3FDklIPkJ-HmstF8nG0dESivxDuLTDeeV4ZBaBS209wL00f5KMuLNuTqj86c9296uSbj5bG8dcXFTzFsmZiK813ntfhsQIpi8GpL_0WJGF2g3LlpJopshk9DWHzj4qUMeL7BOh__btIoN4sg1MEvjzKCMs3rfIzumbMagIr8sYtogIKML2ox74gKWuv73m5AFbK6Vfnwj34FQnDPmb31pG3Oq23TvxLYr-aaHTqBQ

Casting Director

casting_director@gmail.com
passwordDirector8756@

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWY1NDA5MGYyMzM0YjczY2MxZmQiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxMzgzNTI3LCJleHAiOjE3MjE0Njk5MjcsInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwicG9zdDphY3RvcnMiLCJwb3N0OmNhc3RfYWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.lsJlYafIwSZh-RovM6GkHviL5YObqgjPnYZ2T1zch4tnm0muN4DWxUQktoy9COjKNTCxb_mXT8Ykc1XLKatr3UIbAIMF_p1ZFF-2MvlzFBrU2mMVMWrKT5oaePgXqHAU92GBmotaneMM8SQfADkT7blIZcZrgHjnINoXEYw4wMd_28_IHrsXZ8qdFgyT-bTWWUYUjQJ8WpYWj0YCxjv17eQzJk26m1YfBgB89CEHZYJo3or_2Y5RtpKOfqEYnGn7UC-lgS1MIHIDCb-KUWX5r4Mc3uYAfgn7nRfRZNHWQ8nAZv9qk6-oTJp40oe0yUQRQsGVJvwjH0fSLP8ALU7jQg

Executive Producer

executive_producer@gmail.com
passwordProducer4704$

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhkVlVnQnBBdXoxZXVMSHB5Q1REaiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kdWRhdHR4ZzcwdmZkZ2txLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjZlOWY5NTg4ZjJlODZhZjRmOWVlZmYiLCJhdWQiOiJjYXN0aW5nQWdlbmN5QVBJIiwiaWF0IjoxNzIxMzgzNTY5LCJleHAiOjE3MjE0Njk5NjksInNjb3BlIjoiIiwiYXpwIjoidDRvU2toWmhndFRpQTlUY3kxZVI2ZUVZaUY4OFF0WGciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0X2FjdG9ycyIsInBvc3Q6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.FGb1EyXy2UnT6hqgvFwki_DY4c9zmWu90nAJau4Ts5TMNGKEO_Iy65213xc_QV3B4qSgejchzFRAs8H-k0-R8lhxLbGmoJMyXeL1tDfQNbjsC8tY8ZeKAWKhxCYYit8_FaCk2FGawXnPNgU2tpx-GoPRqvn1A__O1Dh9sWMkp7GP00Yh08Tv7PJZbKJZKw_qZQm5Dk_ogYf2oJjNWWE3TcAQGMAWP_kcadlD3Vt4mwWz0CrjcQWqSCvPB2bOrf9AELn1BTx9LIHlsCIsifqtAA0FbQCJ3EYCNFYGMqzrW87WXQVsjccaJdSGm3SBPqXJTL9oe9vUb-u4qEsvcHmcMg



login here to get new tokens if required
`https://dev-dudattxg70vfdgkq.au.auth0.com/authorize?audience=castingAgencyAPI&response_type=token&client_id=t4oSkhZhgtTiA9Tcy1eR6eEYiF88QtXg&redirect_uri=http://127.0.0.1:8080/login-results`

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

The API will return x error types when requests fail:
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
- Returns a success value and a list of actors cast in the movie.
- Private endpont, requires the `view:movies` permission.
- Request Arguments: a decoded JWT token payload and the movie id.
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

> #### GenreEnum List
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
    - release_date: date a valid date format e.g. "dd-mm-YYYY", optional.
    - genre: string, must match an option in the GenreEnum list, optional.

> #### GenreEnum List
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

# Deployment

# Authors

# Acknowledgements


# testing using unittest
[Reference](https://knowledge.udacity.com/questions/788903)

Instructions for running tests





#TODO: test what each endpoint raises and update docstrings
#TODO: how many exceptions to list in docstrings? 405 and 403 for unauthorised access??




# Acknowledgments

Config layout for project ot work with render - https://testdriven.io/blog/flask-render-deployment/

Udacity
