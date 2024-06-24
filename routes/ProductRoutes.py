from flask import Blueprint, jsonify, current_app, request
from services.ProductService import get_note_by_id_service, get_all_note_service, create_note_service, update_note_service, delete_note_service
from werkzeug.utils import secure_filename
import os

notes_bp = Blueprint('products', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@notes_bp.route('/api/v1/notes', methods=['GET'])
def get_notes():
    notes = get_all_note_service()
    notes_list = [{'id': note.id, 'sku': note.sku, 'product_name': note.product_name,  'price': note.price, 'quantity': note.quantity, 'description': note.description, 'product_image': note.product_image} for note in notes]
    return jsonify({'products': notes_list})


@notes_bp.route('/api/v1/notes', methods=['POST'])
def create_note_route():
    if 'product_image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400
    
    file = request.files['product_image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        file.save(image_path)
        relative_image_path = os.path.join('uploads', filename)

        data = request.form
        sku = data.get('sku')
        product_name = data.get('product_name')
        price = data.get('price')
        quantity = data.get('quantity')
        description = data.get('description')

        # if not product_name or not price:
        #     return jsonify({'error': 'sku, product_name, price, quantity and description required'}), 400

        new_note_id = create_note_service(sku, product_name, price, quantity, description, relative_image_path)
        return jsonify({'message': 'note created successfully', 'note_id': new_note_id}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@notes_bp.route('/api/v1/notes/<int:note_id>', methods=['GET'])
def get_note_by_id_route(note_id):
    note = get_note_by_id_service(note_id)
    if note:
        return jsonify({'note': {'id': note.id, 'sku': note.sku, 'product_name': note.product_name, 'price': note.price, 'quantity': note.quantity, 'description': note.description, 'product_image': note.product_image}})
    else:
        return jsonify({'error': 'Note not found'}), 404

@notes_bp.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
def update_note_route(note_id):
    existing_note = get_note_by_id_service(note_id)
    if not existing_note:
        return jsonify({'error': 'Note not found'}), 404

    data = request.form
    sku = data.get('sku')
    product_name = data.get('product_name')
    price = data.get('price')
    quantity = data.get('quantity')
    description = data.get('description')

    # if not product_name or not price:
    #     return jsonify({'error': 'sku, product_name, price, quantity and description required'}), 400

    product_image = existing_note.product_image
    if 'product_image' in request.files:
        file = request.files['product_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product_image = os.path.join('uploads', filename)
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    update_note_service(note_id, sku, product_name, price, quantity, description, product_image)
    return jsonify({'message': 'note updated successfully', 'note_id': note_id})

@notes_bp.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
def delete_note_route(note_id):
        delete_note_service(note_id)
        return jsonify({'message': 'note deleted successfully'})
    
# @notes_bp.route('/api/v1/notes', methods=['POST'])
# def create_note_route():
#     data = request.get_json()
#     product_name = data.get('product_name')
#     image = data.get('image')
#     price = data.get('price')

#     if not product_name or not image or price is None:
#         return jsonify({'error': 'product_name, image and price required'}), 400
    
#     new_note_id = create_note_service(product_name, image, price)
#     return jsonify({'message': 'note created successfully', 'note_id': new_note_id}), 201



# @notes_bp.route('/api/v1/notes/<int:note_id>', methods=['GET'])
# def get_note_by_id_route(note_id):
#     note = get_note_by_id_service(note_id)
#     if note:
#         return jsonify({'note': {'id': note.id, 'product_name': note.product_name, 'image': note.image, 'price': note.price}})
#     else:
#         return jsonify({'error': 'Note not found'}), 404


# @notes_bp.route('/api/v1/notes/<int:note_id>', methods=['PUT'])
# def update_note_route(note_id):
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'No input data provided'}), 400
#     product_name = data.get('product_name')
#     image = data.get('image')
#     price = data.get('price')

#     if not product_name or not image or price is None:
#         return jsonify({'error': 'product_name, image and price required'}), 400
    
#     existing_note= get_note_by_id_service(note_id)
#     if existing_note:
#         update_note_service(note_id, product_name, image, price)
#         return jsonify({'message': 'note update successfully', 'note_id': note_id})
#     else:
#         return jsonify({'error': 'note not found'}), 404
    


# @notes_bp.route('/api/v1/notes/<int:note_id>', methods=['DELETE'])
# def delete_note_route(note_id):
#     existing_note=get_note_by_id_service(note_id)
#     if existing_note:
#         delete_note_service(note_id)
#         return jsonify({'message': 'note deleted successfully'})
#     else:
#         return jsonify({'error': 'note not found'}), 404