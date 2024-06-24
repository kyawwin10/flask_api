import psycopg2

from models.Product import Product


def db_conn():
    return psycopg2.connect(database="flask_project", host="localhost", user="flask", password="flask", port="5432")

def get_all_notes():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM product''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    notes = [Product(id=note[0], sku=note[1], product_name=note[2], price=note[3], quantity=note[4], description=note[5], product_image=note[6]) for note in data]
    return notes

def get_note_by_id(note_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM product WHERE id = %s''', (note_id,))
    note_data = cur.fetchone()
    cur.close()
    conn.close()

    if note_data:
        return Product(id=note_data[0], sku=note_data[1], product_name=note_data[2], price=note_data[3], quantity=note_data[4], description=note_data[5], product_image=note_data[6])
    else:
        return None


def create_note(sku, product_name, price, quantity, description, product_image):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO product (sku, product_name, price, quantity, description, product_image) values (%s, %s, %s,%s, %s, %s) returning *", (sku, product_name, price, quantity, description, product_image))
    new_note_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_note_id

def update_note(id, sku, product_name, price, quantity, description, product_image):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''UPDATE product SET sku=%s, product_name=%s, price=%s, quantity=%s, description=%s, product_image=%s  WHERE id=%s''',(sku, product_name, price, quantity, description, product_image, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_note(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
