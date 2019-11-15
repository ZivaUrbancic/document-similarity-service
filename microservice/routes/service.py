# Embedding Route
# Routes related to creating text embeddings

import sys

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort


#################################################
# Initialize the models
#################################################

from ..library.document_similarity import DocumentSimilarity
from ..library.postgresql import PostgresQL


# get model parameters from the .config file
database_name = app.config['DATABASE NAME']
database_user = app.config['DATABASE_USER']
database_password = app.config['DATABASE_PASSWORD']

# get the rest of parameters from the database
pg = PostgresQL()
pg.connect(database=database_name, user=database_user, password=database_password)

# TODO: update 'embeddings' to the real database name
loaded_embedding = pg.execute("""
        SELECT * FROM embeddings;
    """)

#initialize
similator = DocumentSimilarity(loaded_embedding)

#################################################
# Setup the embeddings blueprint
#################################################

# TODO: provide an appropriate route name and prefix
bp = Blueprint('similarity', __name__, url_prefix='/api/v1/similarity')


@bp.route('/', methods=['GET'])
def index():
    # TODO: provide an appropriate output
    return abort(501)

# TODO: add an appropriate route name                                   # sth like get_closest_documents?
@bp.route('/second', methods=['GET', 'POST'])
def second():
    # TODO: assign the appropriate variables
    variable = None
    if request.method == 'GET':
        # retrieve the correct query parameters
        variable = request.args.get('variable', default='', type=str)
    elif request.method == 'POST':
        # retrieve the text posted to the route
        variable = request.json['variable']
    else:
        # TODO: log exception
        return abort(405)

    try:
        # TODO: add the main functionality with the model and variable
        finish = True
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        # TODO: return the response
        return jsonify({
            "finish": finish
        })
