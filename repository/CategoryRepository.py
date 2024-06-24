import psycopg2
from models.Category import Category

def db_conn():
        return psycopg2.connect(database="flask_project", host="localhost", user="flask", password="flask", port="5432")

def get_all_categories():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM categories''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    category = [Category(id=category[0], category_name=category[1], category_image=category[2], description=category[3]) for category in data]
    return category

def get_category_by_id(category_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM categories WHERE id = %s''', (category_id,))
    category_data = cur.fetchone()
    cur.close()
    conn.close()

    if category_data:
        return Category(id=category_data[0], category_name=category_data[1], category_image=category_data[2], description=category_data[3])
    else:
        return None


def create_category(category_name, category_image, description):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (category_name, category_image, description) values (%s, %s, %s) returning *", (category_name, category_image, description))
    new_category_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_category_id

def update_category(id, category_name, category_image, description):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''UPDATE categories SET category_name=%s, category_image=%s, description=%s WHERE id=%s''',(category_name, category_image, description, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_category(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()