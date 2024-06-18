import os

#TODO look at other projects - i think i've used this before
# Determine the folder of the top-level directory of this project

# coffee shop models.py
project_dir = os.path.dirname(os.path.abspath(__file__))

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    #TODO remove
    # SECRET_KEY = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')

    #TODO Udacity ref

    # usse os.getenv or os.environ.get?
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logging - remove
   # LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL',
                                        # database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,localhost:5432, capstone_test)
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")
    WTF_CSRF_ENABLED = False
