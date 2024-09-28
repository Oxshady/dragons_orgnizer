from flask import Flask, request, jsonify, blueprints
from models import db
from models.categories import Category
from models.users import User
from models.events import Event

app = Flask(__name__)
categories = blueprints.Blueprint('categories', __name__)

@categories.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify({'error': 'No categories found'}), 404
    return jsonify([category.to_dict() for category in categories])

@categories.route('/categories/<int:category_id>', methods['GET'])
def get_category_by_id(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.to_dict())

@categories.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    category = Category(name=name, description=description)
    db.save(category)

@categories.route('/categories/<int:category_id>', methods['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    category.name = name
    category.description = description
    db.save(category)

@categories.route('/categories', methods=['DELETE'])
def delete_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify({'error': 'No categories found'}), 404
    for category in categories:
        db.delete(category)
    return jsonify({'message': 'Categories deleted successfully'})

@categories.route('/categories/<int:category_id>', methods['DELETE'])
def delete_category_by_id(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    db.delete(category)
    return jsonify({'message': 'Category deleted successfully'})
