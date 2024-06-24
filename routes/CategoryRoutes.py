from flask import Blueprint, jsonify, current_app, request
from services.CategoryService import (
    get_all_category_service,
    get_category_by_id_service,
    create_category_service,
    update_category_service,
    delete_category_service
)
from werkzeug.utils import secure_filename
import os

cate_bp = Blueprint('categories', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cate_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = get_all_category_service()
    categories_list = [{'id': c.id, 'category_name': c.category_name, 'category_image': c.category_image, 'description': c.description} for c in categories]
    return jsonify({'Categories': categories_list})

@cate_bp.route('/api/categories', methods=['POST'])
def create_category():
    if 'category_image' not in request.files:
        return jsonify({"message": "No image file part"}), 400

    file = request.files['category_image']
    if file.filename == '':
        return jsonify({"error": "No selected image file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        file.save(image_path)
        relative_image_path = os.path.join('uploads', filename)

        data = request.form
        category_name = data.get('category_name')
        description = data.get('description')


        new_category_id = create_category_service(category_name, relative_image_path, description)
        return jsonify({"message": "Category created!", "Category_id": new_category_id}), 201

    return jsonify({"message": "Invalid file type"}), 400

@cate_bp.route('/api/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = get_category_by_id_service(id)
    if category:
        return jsonify({"id": category.id, "category_name": category.category_name, "category_image": category.category_image, "description": category.description})
    else:
        return jsonify({"message": "Category not found"}), 404

@cate_bp.route('/api/categories/<int:id>', methods=['PUT'])
def update_category_route(id):
    existing_category = get_category_by_id_service(id)
    if not existing_category:
        return jsonify({'error': 'Category page not found'}), 404

    data = request.form
    category_name = data.get('category_name')
    description = data.get('description')

    # if not product_name or not price:
    #     return jsonify({'error': 'product_name and price required'}), 400

    category_image = existing_category.category_image
    if 'category_image' in request.files:
        file = request.files['category_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            category_image = os.path.join('uploads', filename)
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    update_category_service(id, category_name, category_image, description)
    return jsonify({'message': 'Category updated successfully', 'Category_id': id})

@cate_bp.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    delete_category_service(id)
    return jsonify({"message": "Category deleted!"})