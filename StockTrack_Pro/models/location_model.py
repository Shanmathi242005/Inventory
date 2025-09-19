from database import db

class LocationModel:
    def get_all_locations(self):
        conn = db.get_connection()
        locations = conn.execute('SELECT * FROM locations ORDER BY location_name').fetchall()
        conn.close()
        return locations
    
    def get_location(self, location_id):
        conn = db.get_connection()
        location = conn.execute('SELECT * FROM locations WHERE location_id = ?', (location_id,)).fetchone()
        conn.close()
        return location
    
    def add_location(self, location_id, location_name, address, capacity):
        try:
            conn = db.get_connection()
            conn.execute('INSERT INTO locations (location_id, location_name, address, capacity) VALUES (?, ?, ?, ?)',
                        (location_id, location_name, address, int(capacity)))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_location(self, location_id, location_name, address, capacity):
        try:
            conn = db.get_connection()
            conn.execute('UPDATE locations SET location_name = ?, address = ?, capacity = ? WHERE location_id = ?',
                        (location_name, address, int(capacity), location_id))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def delete_location(self, location_id):
        try:
            conn = db.get_connection()
            conn.execute('DELETE FROM locations WHERE location_id = ?', (location_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False