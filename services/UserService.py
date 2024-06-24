from repository.UserRepository import get_user_by_email, create_user

def get_user_by_email_service(email):
    return get_user_by_email(email)

def create_user_service(username, password, phone, email):
    return create_user(username, password, phone, email)