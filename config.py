import os


class Config:
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    # TODO is this needed?
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # TODO Udacity ref

    # usse os.getenv or os.environ.get?
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace(
            "postgres://", "postgresql://", 1
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://postgres:postgres@localhost:5432/capstone"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False
