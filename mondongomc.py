import json
import datetime

from flask import Flask, request, jsonify, make_response
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
mongo = PyMongo(app)


def _document_to_dict(document):
    _document = {}
    for key, value in document.iteritems():
        if isinstance(value, ObjectId):
            _document[key] = str(value)
        elif isinstance(value, datetime.datetime):
            _document[key] = value.isoformat()
        else:
            _document[key] = value
    return _document


def _encode_cursor(cursor):
    documents = []
    for document in cursor:
        documents.append(_document_to_dict(document))
    return documents


def _make_response(results):
    data = {
        'meta': {
            'total_count': len(results)
        },
        'objects': results
    }
    return jsonify(data)


@app.route('/')
@app.route('/<collection>/', methods=['GET', 'POST'])
@app.route('/<collection>/<object_id>/', methods=['GET', 'PUT', 'DELETE'])
def hello_world(collection=None, object_id=None):
    if request.method == 'GET':
        if collection and object_id:
            document = mongo.db[collection].find_one_or_404({'_id': ObjectId(object_id)})

            return jsonify(_document_to_dict(document))
        elif collection and not object_id:
            cursor = mongo.db[collection].find()

            return _make_response(_encode_cursor(cursor))
        else:
            collections = mongo.db.collection_names()
            data = {}

            for collection in collections:
                if collection != 'system.indexes':
                    data[collection] = {
                        'list_endpoint': '/{}/'.format(collection)
                    }

            return jsonify(data)
    elif request.method == 'POST':
        data = json.loads(request.data)
        _id = mongo.db[collection].insert(data)
        document = mongo.db[collection].find_one({'_id': _id})

        return jsonify(_document_to_dict(document))
    elif request.method == 'PUT' and collection and object_id:
        data = json.loads(request.data)
        mongo.db[collection].update({'_id': ObjectId(object_id)}, {"$set": data}, upsert=False)
        document = mongo.db[collection].find_one({'_id': ObjectId(object_id)})

        return jsonify(_document_to_dict(document))
    elif request.method == 'DELETE':
        if collection and object_id:
            mongo.db[collection].remove({'_id': ObjectId(object_id)})
            response = make_response()
            response.status_code = 204
            return response


if __name__ == '__main__':
    app.run(debug=True)
