# Configuration script
# Retrieves the hidden variables from the .env
# file and creates the configuration objects -
# one for each environment.

from dotenv import load_dotenv
load_dotenv()

import os

class Config(object):
    DEBUG = False
    TESTING = False
    CORS = {
        'origins': os.getenv('CORS_ORIGINS').split(',') if os.getenv('CORS_ORIGINS') else None
    }


class ProductionConfig(Config):
    """Production configuration"""

    # TODO: add required secret configurations
    ENV='production'
    SECRET_KEY=os.getenv('PROD_SECRET_KEY')

    # PARAMETERS FOR CONNECTING TO POSTGRES
    ## database with document texts
    DOCUMENTS_DATABASE_NAME=os.getenv('PROD_DOCUMENTS_DATABASE_NAME')
    DOCUMENTS_DATABASE_USER=os.getenv('PROD_DOCUMENTS_DATABASE_USER')
    DOCUMENTS_DATABASE_PASSWORD=os.getenv('PROD_DOCUMENTS_DATABASE_PASSWORD')
    ## database with document embeddings
    EMBEDDINGS_DATABASE_NAME=os.getenv('PROD_EMBEDDINGS_DATABASE_NAME')
    EMBEDDINGS_DATABASE_USER=os.getenv('PROD_EMBEDDINGS_DATABASE_USER')
    EMBEDDINGS_DATABASE_PASSWORD=os.getenv('PROD_EMBEDDINGS_DATABASE_PASSWORD')
    ## database with document similarities
    SIMILARITIES_DATABASE_NAME=os.getenv('PROD_SIMILARITIES_DATABASE_NAME')
    SIMILARITIES_DATABASE_USER=os.getenv('PROD_SIMILARITIES_DATABASE_USER')
    SIMILARITIES_DATABASE_PASSWORD=os.getenv('PROD_SIMILARITIES_DATABASE_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""

    # TODO: add required secret configurations
    ENV='development'
    DEBUG = True
    SECRET_KEY=os.getenv('DEV_SECRET_KEY')

    # PARAMETERS FOR CONNECTING TO POSTGRES
    DOCUMENTS_DATABASE_NAME=os.getenv('DEV_DOCUMENTS_DATABASE_NAME')
    DOCUMENTS_DATABASE_USER=os.getenv('DEV_DOCUMENTS_DATABASE_USER')
    DOCUMENTS_DATABASE_PASSWORD=os.getenv('DEV_DOCUMENTS_DATABASE_PASSWORD')
    ## database with document embeddings
    EMBEDDINGS_DATABASE_NAME=os.getenv('DEV_EMBEDDINGS_DATABASE_NAME')
    EMBEDDINGS_DATABASE_USER=os.getenv('DEV_EMBEDDINGS_DATABASE_USER')
    EMBEDDINGS_DATABASE_PASSWORD=os.getenv('DEV_EMBEDDINGS_DATABASE_PASSWORD')
    ## database with document similarities
    SIMILARITIES_DATABASE_NAME=os.getenv('DEV_SIMILARITIES_DATABASE_NAME')
    SIMILARITIES_DATABASE_USER=os.getenv('DEV_SIMILARITIES_DATABASE_USER')
    SIMILARITIES_DATABASE_PASSWORD=os.getenv('DEV_SIMILARITIES_DATABASE_PASSWORD')


class TestingConfig(Config):
    """Testing configuration"""

    # TODO: add required secret configurations
    ENV='testing'
    TESTING = True
    SECRET_KEY=os.getenv('TEST_SECRET_KEY')

    # PARAMETERS FOR CONNECTING TO POSTGRES
    DOCUMENTS_DATABASE_NAME=os.getenv('TEST_DOCUMENTS_DATABASE_NAME')
    DOCUMENTS_DATABASE_USER=os.getenv('TEST_DOCUMENTS_DATABASE_USER')
    DOCUMENTS_DATABASE_PASSWORD=os.getenv('TEST_DOCUMENTS_DATABASE_PASSWORD')
    ## database with document embeddings
    EMBEDDINGS_DATABASE_NAME=os.getenv('TEST_EMBEDDINGS_DATABASE_NAME')
    EMBEDDINGS_DATABASE_USER=os.getenv('TEST_EMBEDDINGS_DATABASE_USER')
    EMBEDDINGS_DATABASE_PASSWORD=os.getenv('TEST_EMBEDDINGS_DATABASE_PASSWORD')
    ## database with document similarities
    SIMILARITIES_DATABASE_NAME=os.getenv('TEST_SIMILARITIES_DATABASE_NAME')
    SIMILARITIES_DATABASE_USER=os.getenv('TEST_SIMILARITIES_DATABASE_USER')
    SIMILARITIES_DATABASE_PASSWORD=os.getenv('TEST_SIMILARITIES_DATABASE_PASSWORD')
