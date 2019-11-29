# Document comparison Route
# Routes related to comparing documents among eachother

from flask import (
    Blueprint, request, jsonify, current_app as app
)
from werkzeug.exceptions import abort


#################################################
# Initialize the models
#################################################

from ..library.document_similarity import DocumentSimilarity
from ..library.postgresql import PostgresQL


# GET MODEL PARAMETERS FROM THE .config FILE
# database with document texts
database_name = app.config['DATABASE_NAME']
database_user = app.config['DATABASE_USER']
database_password = app.config['DATABASE_PASSWORD']
# url to text embedding service
text_embedding_url = app.config['TEXT_EMBEDDING_URL']

# Connect to the embeddings database and retrieve the embeddings:
pg_embeddings = PostgresQL()
pg_embeddings.connect(database=database_name, user=database_user,
                      password=database_password)
# TODO: change the expression if needed
loaded_embedding = pg_embeddings.execute("""
        SELECT * FROM embeddings;
    """)
indices = [embedding['document_id'] for embedding in loaded_embedding]
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
        pg.connect(database=database_name, user=database_user,
                   password=database_password)
        # TODO: change the expression if needed
        document_text = pg.execute("""
        SELECT document_text FROM documents WHERE document_id={};
        """.format(doc_id))

        # Call the text-embedding-service and produce the embedding
        # TODO: add language_model parameter
        params = {'text': document_text}
        new_embedding = request.get(url=text_embedding_url, params=params)['embedding']

        # Using DocumentSimilarity compute similarities and return them
        similarity = DocumentSimilarity(embedding=embeddings, indices=indices)
        additional_similarities = similarity.new_document(doc_id, new_embedding)

        # insert a new embedding into the database
        pg.execute("""
            INSERT INTO embeddings
            VALUES ({}, {})
            """.format(doc_id, new_embedding))

        # insert similarities into the database
        for i, j, sim in additional_similarities:
            pg.execute("""
                INSERT INTO embeddings
                VALUES ({}, {}, {})
                """.format(i, j, sim))

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
            SELECT document2 FROM similarities
            WHERE document1 = {}
            ORDER BY sim DESC;
            """.format(doc_id))
        result_indices = [entry['document2'] for entry in similarity_list[:k]]
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
