# Embedding Route
# Routes related to creating text embeddings

import sys
import numpy

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort
from operator import itemgetter


#################################################
# Initialize the models
#################################################

from ..library.document_similarity import DocumentSimilarity
from ..library.postgresql import PostgresQL


# GET MODEL PARAMETERS FROM THE .config FILE ####
# database with document texts
documents_database_name = app.config['DOCUMENTS_DATABASE_NAME']
documents_database_user = app.config['DOCUMENTS_DATABASE_USER']
documents_database_password = app.config['DOCUMENTS_DATABASE_PASSWORD']
# database with document embeddings
embeddings_database_name = app.config['EMBEDDINGS_DATABASE_NAME']
embeddings_database_user = app.config['EMBEDDINGS_DATABASE_USER']
embeddings_database_password = app.config['EMBEDDINGS_DATABASE_PASSWORD']
# database with document similarities
similarities_database_name = app.config['SIMILARITIES_DATABASE_NAME']
similarities_database_user = app.config['SIMILARITIES_DATABASE_USER']
similarities_database_password = app.config['SIMILARITIES_DATABASE_PASSWORD']


# Connect to the embeddings database and retrieve the embeddings:
pg_embeddings = PostgresQL()
pg_embeddings.connect(database=embeddings_database_name, user=embeddings_database_user,
                      password=embeddings_database_password)
# TODO: change the expression if needed
loaded_embedding = pg_embeddings.execute("""
        SELECT * FROM embeddings;
    """)
indices = [embedding['embedding_id'] for embedding in loaded_embedding]
embeddings = [embedding['embedding'] for embedding in loaded_embedding]



#################################################
# Setup the embeddings blueprint
#################################################

# TODO: provide an appropriate route name and prefix
bp = Blueprint('similarity', __name__, url_prefix='/api/v1/similarity')


@bp.route('/', methods=['GET'])
def index():
    # TODO: provide an appropriate output
    return abort(501)

@bp.route('/new_document_embedding', methods=['GET', 'POST'])
def update_similarities():
    # TODO: write documentation
    # get document id as the parameter
    doc_id = None
    if request.method == 'GET':
        # retrieve new document's id
        doc_id = request.args.get('document_id', default=None, type=int)
    elif request.method == 'POST':
        # retrieve the text posted to the route
        doc_id = request.json['document_id']
    else:
        # TODO: log exception
        return abort(405)

    try:
        # retrieve the document's text
        pg = PostgresQL()
        pg.connect(database=documents_database_name, user=documents_database_user,
                   password=documents_database_password)
        # TODO: change the expression if needed
        document_text = pg.execute("""
        SELECT * FROM documents WHERE document_id={};
        """.format(doc_id))

        # TODO: Call the text-embedding-service and produce the embedding
        new_embedding = None

        # Using DocumentSimilarity compute similarities and return them
        similarity = DocumentSimilarity(embedding=embeddings, indices=indices)
        additional_similarities = similarity.new_document(doc_id, new_embedding)

        # TODO: Add the new embedding and similarities to the databases

        finish = True
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        # TODO: return the response
        return jsonify({
            "additional similarities": additional_similarities,
            "finish": finish
        })

@bp.route('/get_similarities', methods=['GET', 'POST'])
def get_similarities():
    # TODO: write documentation
    doc_id = None
    k = None
    if request.method == 'GET':
        # retrieve the correct query parameters
        doc_id = request.args.get('document_id', default=None, type=int)
        k = request.args.get('get_k', default=None, type=int)
    elif request.method == 'POST':
        # retrieve the text posted to the route
        doc_id = request.json['document_id']
        k = request.json['get_k']
    else:
        # TODO: log exception
        return abort(405)

    try:
        # retrieve the similarity matrix
        pg = PostgresQL()
        pg.connect(database=similarities_database_name, user=similarities_database_user,
                   password=similarities_database_password)
        # TODO: change the expression if needed
        similarity_matrix = pg.execute("""
        SELECT * FROM similarity;
        """)

        # make a dictionary {document_id: similarity with focus document} of candidates
        candidates = {}
        for line in similarity_matrix[(similarity_matrix[:, 0] == doc_id)]:
            candidates[line[1]] = line[2]
        # sort the entries, keep the k entries with biggest similarities, only keep document ids
        result_indices = [i for i, j in sorted(candidates.items(), key=itemgetter(1), reverse=True)[:k]]
        finish = True
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        return jsonify({
            "similar_documents": result_indices,
            "finish": finish
        })
