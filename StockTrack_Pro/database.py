import sqlite3
import os
from datetime import datetime

class InventoryDB:
    def __init__(self):
        self.db_name = "stocktrack.db"
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        if os.path.exists(self.db_name):
            return
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Locations table
        cursor.execute('''
            CREATE TABLE locations (
                location_id TEXT PRIMARY KEY,
                location_name TEXT NOT NULL,
                address TEXT,
                capacity INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Movements table
        cursor.execute('''
            CREATE TABLE product_movements (
                movement_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                from_location TEXT,
                to_location TEXT,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                notes TEXT,
                FOREIGN KEY (from_location) REFERENCES locations(location_id),
                FOREIGN KEY (to_location) REFERENCES locations(location_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert sample data
        self.insert_sample_data()
    
    def insert_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sample products
        products = [
            ('P001', 'iPhone 13', 'Latest iPhone model with A15 Bionic chip'),
            ('P002', 'Samsung Galaxy S21', 'Flagship Samsung phone with 120Hz display'),
            ('P003', 'MacBook Pro', 'Apple laptop for professionals with M1 chip'),
            ('P004', 'Dell XPS 15', 'High-performance Windows laptop for creators')
        ]
        
        cursor.executemany('''
            INSERT INTO products (product_id, product_name, description)
            VALUES (?, ?, ?)
        ''', products)
        
        # Sample locations
        locations = [
            ('L001', 'Main Warehouse', '123 Storage Street, Industrial Area', 5000),
            ('L002', 'Retail Store Downtown', '456 Market Avenue, City Center', 1000),
            ('L003', 'Westside Outlet', '789 Shopping Road, West District', 800),
            ('L004', 'Repair & Service Center', '321 Tech Boulevard, Service Zone', 300)
        ]
        
        cursor.executemany('''
            INSERT INTO locations (location_id, location_name, address, capacity)
            VALUES (?, ?, ?, ?)
        ''', locations)
        
        # Sample movements
        movements = [
            ('MOV001', None, 'L001', 'P001', 100, 'Initial stock received'),
            ('MOV002', None, 'L001', 'P002', 80, 'Initial stock received'),
            ('MOV003', 'L001', 'L002', 'P001', 20, 'Stock transfer to retail store'),
            ('MOV004', 'L001', 'L002', 'P002', 15, 'Stock transfer to retail store')
        ]
        
        cursor.executemany('''
            INSERT INTO product_movements (movement_id, from_location, to_location, product_id, quantity, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', movements)
        
        conn.commit()
        conn.close()

# Create database instance
db = InventoryDB()