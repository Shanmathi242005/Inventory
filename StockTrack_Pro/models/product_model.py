from database import db

class ProductModel:
    def get_all_products(self):
        conn = db.get_connection()
        products = conn.execute('SELECT * FROM products ORDER BY product_name').fetchall()
        conn.close()
        return products
    
    def get_product(self, product_id):
        conn = db.get_connection()
        product = conn.execute('SELECT * FROM products WHERE product_id = ?', (product_id,)).fetchone()
        conn.close()
        return product
    
    def add_product(self, product_id, product_name, description):
        try:
            conn = db.get_connection()
            conn.execute('INSERT INTO products (product_id, product_name, description) VALUES (?, ?, ?)',
                        (product_id, product_name, description))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product(self, product_id, product_name, description):
        try:
            conn = db.get_connection()
            conn.execute('UPDATE products SET product_name = ?, description = ? WHERE product_id = ?',
                        (product_name, description, product_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def delete_product(self, product_id):
        try:
            conn = db.get_connection()
            conn.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False