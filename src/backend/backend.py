#!/usr/bin/env python3
import datetime
import os
import pymongo
from bson import ObjectId
from flask import make_response
from flask import Flask, jsonify
from flask_restful import reqparse
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
app_port = os.getenv("PORT", 8001)

# Mongo DB Connection
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 27017))
client = MongoClient(db_host, db_port)
db = client['mydb']
collection = db['deploys']

# Parser
parser = reqparse.RequestParser()
parser.add_argument('componente')
parser.add_argument('versao')
parser.add_argument('responsavel')
parser.add_argument('status')


@app.route('/api/deploys', methods=['GET'])
def get():
    try:
        query = collection.find().sort('_id', pymongo.DESCENDING)
        docs = dumps(query)
        app.logger.info("{}".format(docs))
        return (docs)
    except Exception as e:
        app.logger.error(e)


@app.route('/api/deploys/<id>', methods=['GET'])
def get_deploy(id):
    try:
        query = collection.find({"_id": ObjectId(id)})
        docs = dumps(query)
        app.logger.info("{}".format(docs))
        return (docs)
    except Exception as e:
        app.logger.error(e)


@app.route('/api/deploys', methods=['POST'])
def post():
    try:
        args = parser.parse_args()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc = {'componente': args['componente'],
               'versao': args['versao'],
               'responsavel': args['responsavel'],
               'status': args['status'],
               'criado': f"{date}",
               'atualizado': ''}
        res = collection.insert_one(doc).inserted_id
        app.logger.info("ID: {}, Payload: {}".format(res, doc))
        return jsonify({"status_code": "201", "id": "{}".format(res)}), 201
    except Exception as e:
        app.logger.error(e)


@app.route('/api/deploys/<id>', methods=['PUT'])
def put(id):
    try:
        args = parser.parse_args()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        collection.update_one({"_id": ObjectId(id)},
                              {"$set": {'status': args['status'],
                                        'atualizado': f"{date}"}})
        app.logger.info("ID: {}".format(id))
        return jsonify({"status_code": "200", "id": "{}".format(id)})
    except Exception as e:
        app.logger.error(e)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=app_port)
