import os
from pathlib import Path

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

app = Flask(__name__)
CORS(app)

MONGODB_URI = os.getenv(
    'MONGODB_URI', 'mongodb://127.0.0.1:27017/class7_products')
PORT = int(os.getenv('PORT', '5000'))

client = MongoClient(MONGODB_URI)
db = client.get_database()
products_collection = db.products


@app.get('/health')
def health_check():
    return jsonify({'status': 'ok'})


@app.get('/openapi.yaml')
def openapi_spec():
    return send_from_directory(BASE_DIR, 'openapi.yaml')


def to_product_doc(document):
    return {
        'id': str(document['_id']),
        'name': document.get('name'),
        'description': document.get('description', ''),
        'price': document.get('price'),
        'in_stock': document.get('in_stock', True),
    }


def validate_product_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return 'JSON body must be an object'

    required_fields = ['name', 'price']
    if not partial:
        for field in required_fields:
            if field not in payload:
                return f'Missing required field: {field}'

    if 'name' in payload and (not isinstance(payload['name'], str) or not payload['name'].strip()):
        return 'name must be a non-empty string'

    if 'price' in payload and not isinstance(payload['price'], (int, float)):
        return 'price must be a number'

    if 'in_stock' in payload and not isinstance(payload['in_stock'], bool):
        return 'in_stock must be a boolean'

    if 'description' in payload and not isinstance(payload['description'], str):
        return 'description must be a string'

    return None


@app.get('/api/v1/products')
def get_products():
    try:
        products = [to_product_doc(
            item) for item in products_collection.find().sort('_id', -1)]
        return jsonify(products), 200
    except PyMongoError as error:
        return jsonify({'message': 'Database error', 'error': str(error)}), 500


@app.get('/api/v1/products/<product_id>')
def get_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({'message': 'Invalid product id'}), 400

    try:
        document = products_collection.find_one({'_id': ObjectId(product_id)})
        if not document:
            return jsonify({'message': 'Product not found'}), 404

        return jsonify(to_product_doc(document)), 200
    except PyMongoError as error:
        return jsonify({'message': 'Database error', 'error': str(error)}), 500


@app.post('/api/v1/products')
def create_product():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({'message': 'JSON body must be an object'}), 400

    error_message = validate_product_payload(payload)
    if error_message:
        return jsonify({'message': error_message}), 400

    product_data = {
        'name': payload['name'].strip(),
        'description': payload.get('description', ''),
        'price': float(payload['price']),
        'in_stock': payload.get('in_stock', True),
    }

    try:
        result = products_collection.insert_one(product_data)
        document = products_collection.find_one({'_id': result.inserted_id})
        return jsonify(to_product_doc(document)), 201
    except PyMongoError as error:
        return jsonify({'message': 'Database error', 'error': str(error)}), 500


@app.put('/api/v1/products/<product_id>')
def update_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({'message': 'Invalid product id'}), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({'message': 'JSON body must be an object'}), 400

    error_message = validate_product_payload(payload, partial=False)
    if error_message:
        return jsonify({'message': error_message}), 400

    update_data = {
        'name': payload['name'].strip(),
        'description': payload.get('description', ''),
        'price': float(payload['price']),
        'in_stock': payload.get('in_stock', True),
    }

    try:
        result = products_collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data},
        )

        if result.matched_count == 0:
            return jsonify({'message': 'Product not found'}), 404

        document = products_collection.find_one({'_id': ObjectId(product_id)})
        return jsonify(to_product_doc(document)), 200
    except PyMongoError as error:
        return jsonify({'message': 'Database error', 'error': str(error)}), 500


@app.delete('/api/v1/products/<product_id>')
def delete_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({'message': 'Invalid product id'}), 400

    try:
        result = products_collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({'message': 'Product not found'}), 404

        return '', 204
    except PyMongoError as error:
        return jsonify({'message': 'Database error', 'error': str(error)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
