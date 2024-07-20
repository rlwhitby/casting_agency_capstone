# is this good practice? find reference
""" The Valid_ constants are set to pass a known valid
information (id, post or patch body) to the unit test cases that expect them

The Invalid_ constants are set to pass a known invalid
information (id, post or patch body) to the unit test cases that expect them

"""
VALID_MOVIE_ID = 1
VALID_ACTOR_ID = 1
INVALID_MOVIE_ID = 1000
INVALID_ACTOR_ID = 1000

VALID_ACTOR = {
    "name": "Michelle Yeoh",
    "age": 61,
    "gender": "Female"
    }

INVALID_ACTOR = {
    "name": "Michelle Yeoh",
    "gender": "Female"
    }

VALID_ACTOR_PATCH = {
    "name": "Tom Holland",
    "age": 28,
    "gender": "Male"
    }

VALID_MOVIE = {
    "title": "Crazy Rich Asians",
    "release_date": "2018-08-15",
    "genre": "Comedy",
}
INVALID_MOVIE = {
    "title": "Everything Everywhere All at Once",
    "genre": "Action"
    }

VALID_MOVIE_PATCH = {
    "title": "The Impossible",
    "release_date": "2012-09-09",
    "genre": "Drama",
}
