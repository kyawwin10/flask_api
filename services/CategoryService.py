from repository.CategoryRepository import get_all_categories, get_category_by_id, create_category, update_category, delete_category

def get_all_category_service():
    return get_all_categories()

def get_category_by_id_service(id):
    return get_category_by_id(id)

def create_category_service(category_name, category_image, description):
    return create_category(category_name, category_image, description)

def update_category_service(id, category_name, category_image, description):
    update_category(id, category_name, category_image, description)

def delete_category_service(id):
    delete_category(id)