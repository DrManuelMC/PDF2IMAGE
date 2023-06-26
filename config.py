import os
from dotenv import load_dotenv, find_dotenv


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "xxx"

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = os.getenv("DEBUG")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    ENV = os.getenv("ENV")
    TESTING = False

    # caminhos padrão
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_PATH = os.path.join(BASE_PATH, 'output')

    