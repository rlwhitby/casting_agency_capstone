import os


class Config:
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    # TODO is this needed?
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # TODO Udacity ref

    # use os.getenv or os.environ.get?
    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace(
            "postgres://", "postgresql://", 1
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql://postgres:postgres@localhost:5432/capstone"
        )
        # SQLALCHEMY_DATABASE_URI = os.getenv(
        #     "DATABASE_URL",
        #     default="postgresql://postgres:postgres@localhost:5432/capstone",
        # )
        SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        default="postgresql://postgres:postgres@localhost:5432/capstone_test",
    )
