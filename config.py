import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Development(object):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('BASE_USER')}:" \
                              f"{os.getenv('BASE_PASS')}@{os.getenv('BASE_HOST')}/{os.getenv('BASE_BASE')}"
    REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0?db=1"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    FLASK_SECRET = os.getenv("FLASK_SECRET", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_POOL_TIMEOUT = 200
    SQLALCHEMY_MAX_OVERFLOW = 50
    STATIC_FOLDER = os.path.join(BASEDIR, "static")
    TEMPLATES_FOLDER = os.path.join(BASEDIR, "templates")


class Production(Development):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = os.getenv("SERVER_NAME", "localhost")
