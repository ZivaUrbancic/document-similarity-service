# Document comparison Route
# Routes related to comparing documents among eachother

from flask import (
    Blueprint, request, jsonify, current_app as app
)
from werkzeug.exceptions import abort
import requests
import json

#################################################
# Initialize the models
#################################################

from ..library.document_similarity import DocumentSimilarity
from ..library.postgresql import PostgresQL


user_message = "Everything went fine. Enjoy using our service."


# GET MODEL PARAMETERS FROM THE .config FILE
# database with document texts
database_name = app.config['DATABASE_NAME']
database_user = app.config['DATABASE_USER']
database_password = app.config['DATABASE_PASSWORD']
# url to text embedding service
text_embedding_url = app.config['TEXT_EMBEDDING_URL']

# Connect to the embeddings database and retrieve the embeddings:
pg = PostgresQL()
pg.connect(database=database_name, user=database_user,
                      password=database_password)


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
    if request.method == 'GET':
        # retrieve new document's id
        try:
            doc_id = request.args.get('document_id', default=None, type=int)
        except Exception as e:
            return abort(401, e)
    elif request.method == 'POST':
        try:
            # retrieve the text posted to the route
            doc_id = request.json['document_id']
        except Exception as e:
            return abort(401, str(e))
    else:
        # TODO: log exception
        return abort(405)

    # get embeddings from postgres
    # TODO: change the expression if needed
    try:
        loaded_embedding = pg.execute("""
            SELECT * FROM document_embeddings;
            """)

        indices = [embedding['document_id'] for embedding in loaded_embedding]
        embeddings = [embedding['vector'] for embedding in loaded_embedding]
    except Exception as e:
        return abort(404, str(e))

    try:
        # retrieve the document's text
        # TODO: change the expression if needed
        try:
            statement = """
                SELECT fulltext_cleaned FROM documents
                WHERE document_id={};
                """.format(doc_id)
            document_text = (pg.execute(statement))[0]['fulltext_cleaned']
        except Exception as e:
            return abort(400, "Could not retrieve text of the document from the database. "+str(e))

        # Call the text-embedding-service and produce the embedding
        # TODO: add language_model parameter
        try:
            params = {'text': document_text, 'language': 'en'}
            service_response = requests.post(url=text_embedding_url, json=params).json()
            new_embedding = service_response['embedding']
        except Exception as e:
            return abort(400, "Could not retrieve the embedding from the text embedding service. " + str(e))

        # Using DocumentSimilarity compute similarities and return them
        similarity = DocumentSimilarity(embedding=embeddings, indices=indices)
        additional_similarities = similarity.new_document(doc_id, new_embedding)

        # insert a new embedding into the database
        # pg.execute("""
        #     INSERT INTO embeddings
        #     VALUES ({}, {})
        #     """.format(doc_id, new_embedding))

        # # insert similarities into the database
        # for i, j, sim in additional_similarities:
        #     pg.execute("""
        #         INSERT INTO similarities
        #         VALUES ({}, {}, {})
        #         """.format(i, j, sim))

        finish = True
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        # TODO: return the response
        additional_similarities = "TODO"
        return jsonify({
            "embedding": new_embedding,
            "additional similarities": additional_similarities,
            "indices": indices,
            "finish": finish
        })

@bp.route('/get_similarities', methods=['GET', 'POST'])
def get_similarities():
    # TODO: write documentation
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
        pg.connect(database=database_name, user=database_user,
                   password=database_password)
        # TODO: change the expression if needed
        # get only the lines in table 'similarities' where the first document has id doc_id
        # sort them by the similarity column, descending
        similarity_list = pg.execute("""
            SELECT document2_id FROM similarities
            WHERE document1_id = {}
            ORDER BY similarity_score DESC;
            """.format(doc_id))
        result_indices = [entry['document2_id'] for entry in similarity_list[:k]]
        finish = True
    except Exception as e:
        # TODO: log exception
        # something went wrong with the request
        return abort(400, str(e))
    else:
        return jsonify({
            "similar_documents": result_indices,
            "length_similarity_list": len(similarity_list),
            "finish": finish
        })
