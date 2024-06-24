# import psycopg2

# conn = "postgres".connect(database="flask_project", host="localhost", user="flask", password="flask", port="5432")
# cur = conn.cursor()

# cur.execute(''' CREATE TABLE IF EXISTS public.product(id serial PRIMARY KEY, product_name text(500), image text, price integer(100)) ''')
# cur.execute('''INSERT INTO product (product_name, image, price) VALUES ('product_name', 'image', 'price')''')
# conn.commit()

# cur.close()
# conn.close()