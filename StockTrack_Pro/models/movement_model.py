from database import db

class MovementModel:
    def get_all_movements(self):
        conn = db.get_connection()
        movements = conn.execute('''
            SELECT pm.*, p.product_name, 
                   fl.location_name as from_location_name, 
                   tl.location_name as to_location_name
            FROM product_movements pm
            LEFT JOIN products p ON pm.product_id = p.product_id
            LEFT JOIN locations fl ON pm.from_location = fl.location_id
            LEFT JOIN locations tl ON pm.to_location = tl.location_id
            ORDER BY pm.timestamp DESC
        ''').fetchall()
        conn.close()
        return movements
    
    def get_movement(self, movement_id):
        conn = db.get_connection()
        movement = conn.execute('''
            SELECT pm.*, p.product_name, 
                   fl.location_name as from_location_name, 
                   tl.location_name as to_location_name
            FROM product_movements pm
            LEFT JOIN products p ON pm.product_id = p.product_id
            LEFT JOIN locations fl ON pm.from_location = fl.location_id
            LEFT JOIN locations tl ON pm.to_location = tl.location_id
            WHERE pm.movement_id = ?
        ''', (movement_id,)).fetchone()
        conn.close()
        return movement
    
    def add_movement(self, movement_id, from_location, to_location, product_id, quantity, notes):
        try:
            conn = db.get_connection()
            conn.execute('''
                INSERT INTO product_movements (movement_id, from_location, to_location, product_id, quantity, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (movement_id, from_location, to_location, product_id, quantity, notes))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def update_movement(self, movement_id, from_location, to_location, product_id, quantity, notes):
        try:
            conn = db.get_connection()
            conn.execute('''
                UPDATE product_movements 
                SET from_location = ?, to_location = ?, product_id = ?, quantity = ?, notes = ?
                WHERE movement_id = ?
            ''', (from_location, to_location, product_id, quantity, notes, movement_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def delete_movement(self, movement_id):
        try:
            conn = db.get_connection()
            conn.execute('DELETE FROM product_movements WHERE movement_id = ?', (movement_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False