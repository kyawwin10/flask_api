import psycopg2

from models.User import User

def db_conn():
    return psycopg2.connect(database="flask_project", host="localhost", user="flask", password="flask", port="5432")

def get_all_usernames():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    usernames = [User(username=user[0], password=user[1], phone=user[2], email=user[3]) for user in usernames]
    return usernames

def get_user_by_email(email):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE email = %s''', (email,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()

    if user_data:
        return User(username=user_data[0], password=user_data[1], phone=user_data[2], email=user_data[3])
    else:
        return None
    
def create_user(username, password, phone, email):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, phone, email) VALUES (%s, %s, %s, %s) RETURNING *", (username, password, phone, email))
    new_user_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_user_id