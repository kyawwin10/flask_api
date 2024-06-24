from repository.ProductRepository import get_all_notes, get_note_by_id, create_note, update_note, delete_note

def get_all_note_service():
    return get_all_notes()

def get_note_by_id_service(id):
    return get_note_by_id(id)

def create_note_service(sku, product_name, price, quantity, description, product_image):
    return create_note(sku, product_name, price, quantity, description, product_image)

def update_note_service(id, sku, product_name, price, quantity, description, product_image):
    update_note(id, sku, product_name, price, quantity, description, product_image)

def delete_note_service(id):
    delete_note(id)