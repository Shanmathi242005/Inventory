from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'stocktrack_pro_secret_key_2024_unique'

print("🔧 Initializing StockTrack Pro...")

# Database setup
def init_db():
    try:
        conn = sqlite3.connect('stocktrack.db')
        c = conn.cursor()
        
        # Create Products table
        c.execute('''CREATE TABLE IF NOT EXISTS products
                    (product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, description TEXT)''')
        
        # Create Locations table
        c.execute('''CREATE TABLE IF NOT EXISTS locations
                    (location_id TEXT PRIMARY KEY, location_name TEXT NOT NULL, address TEXT, capacity INTEGER)''')
        
        # Create Movements table
        c.execute('''CREATE TABLE IF NOT EXISTS product_movements
                    (movement_id TEXT PRIMARY KEY, timestamp TEXT, from_location TEXT,
                     to_location TEXT, product_id TEXT, quantity INTEGER, notes TEXT)''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        
        # Insert sample data
        insert_sample_data()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def insert_sample_data():
    try:
        conn = sqlite3.connect('stocktrack.db')
        c = conn.cursor()
        
        # Check if sample data already exists
        c.execute("SELECT COUNT(*) FROM products")
        product_count = c.fetchone()[0]
        
        if product_count == 0:
            # Sample products
            products = [
                ('P001', 'iPhone 13', 'Latest iPhone model'),
                ('P002', 'Samsung Galaxy S21', 'Flagship Samsung phone'),
                ('P003', 'MacBook Pro', 'Apple laptop for professionals'),
                ('P004', 'Dell XPS 15', 'High-performance Windows laptop')
            ]
            
            c.executemany('INSERT INTO products VALUES (?, ?, ?)', products)
            
            # Sample locations
            locations = [
                ('L001', 'Main Warehouse', '123 Storage St', 1000),
                ('L002', 'Retail Store', '456 Market Ave', 200),
                ('L003', 'Outlet Store', '789 Outlet Rd', 150)
            ]
            
            c.executemany('INSERT INTO locations VALUES (?, ?, ?, ?)', locations)
            
            # Sample movements
            movements = [
                ('MOV001', '2024-01-01 10:00:00', None, 'L001', 'P001', 100, 'Initial stock'),
                ('MOV002', '2024-01-01 11:00:00', None, 'L001', 'P002', 80, 'Initial stock'),
                ('MOV003', '2024-01-02 09:00:00', 'L001', 'L002', 'P001', 20, 'Store transfer')
            ]
            
            c.executemany('INSERT INTO product_movements VALUES (?, ?, ?, ?, ?, ?, ?)', movements)
            
            conn.commit()
            print("✅ Sample data inserted successfully")
        
    except Exception as e:
        print(f"❌ Sample data error: {e}")
    finally:
        if conn:
            conn.close()

# Initialize database
init_db()

def get_db_connection():
    conn = sqlite3.connect('stocktrack.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Product routes
@app.route('/products')
def products_list():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY product_name').fetchall()
    conn.close()
    return render_template('products/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id'].strip()
        product_name = request.form['product_name'].strip()
        description = request.form.get('description', '').strip()
        
        if not product_id or not product_name:
            flash('Product ID and Name are required!', 'error')
            return render_template('products/add.html')
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO products (product_id, product_name, description) VALUES (?, ?, ?)',
                        (product_id, product_name, description))
            conn.commit()
            flash('✅ Product added successfully!', 'success')
            return redirect(url_for('products_list'))
        except sqlite3.IntegrityError:
            flash('❌ Product ID already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('products/add.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        product_name = request.form['product_name'].strip()
        description = request.form.get('description', '').strip()
        
        try:
            conn.execute('UPDATE products SET product_name = ?, description = ? WHERE product_id = ?',
                        (product_name, description, product_id))
            conn.commit()
            flash('✅ Product updated successfully!', 'success')
            return redirect(url_for('products_list'))
        except:
            flash('❌ Error updating product!', 'error')
        finally:
            conn.close()
    
    product = conn.execute('SELECT * FROM products WHERE product_id = ?', (product_id,)).fetchone()
    conn.close()
    
    if not product:
        flash('❌ Product not found!', 'error')
        return redirect(url_for('products_list'))
    
    return render_template('products/edit.html', product=product)

# Location routes
@app.route('/locations')
def locations_list():
    conn = get_db_connection()
    locations = conn.execute('SELECT * FROM locations ORDER BY location_name').fetchall()
    conn.close()
    return render_template('locations/list.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id'].strip()
        location_name = request.form['location_name'].strip()
        address = request.form.get('address', '').strip()
        capacity = request.form.get('capacity', '100')
        
        if not location_id or not location_name:
            flash('Location ID and Name are required!', 'error')
            return render_template('locations/add.html')
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO locations (location_id, location_name, address, capacity) VALUES (?, ?, ?, ?)',
                        (location_id, location_name, address, int(capacity)))
            conn.commit()
            flash('✅ Location added successfully!', 'success')
            return redirect(url_for('locations_list'))
        except sqlite3.IntegrityError:
            flash('❌ Location ID already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('locations/add.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        location_name = request.form['location_name'].strip()
        address = request.form.get('address', '').strip()
        capacity = request.form.get('capacity', '100')
        
        try:
            conn.execute('UPDATE locations SET location_name = ?, address = ?, capacity = ? WHERE location_id = ?',
                        (location_name, address, int(capacity), location_id))
            conn.commit()
            flash('✅ Location updated successfully!', 'success')
            return redirect(url_for('locations_list'))
        except:
            flash('❌ Error updating location!', 'error')
        finally:
            conn.close()
    
    location = conn.execute('SELECT * FROM locations WHERE location_id = ?', (location_id,)).fetchone()
    conn.close()
    
    if not location:
        flash('❌ Location not found!', 'error')
        return redirect(url_for('locations_list'))
    
    return render_template('locations/edit.html', location=location)

# Movement routes
@app.route('/movements')
def movements_list():
    conn = get_db_connection()
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
    return render_template('movements/list.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    conn = get_db_connection()
    
    if request.method == 'POST':
        from_location = request.form['from_location'] if request.form['from_location'] != '' else None
        to_location = request.form['to_location'] if request.form['to_location'] != '' else None
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        notes = request.form.get('notes', '').strip()
        
        if not from_location and not to_location:
            flash('❌ Either From or To location must be specified!', 'error')
            return redirect(url_for('add_movement'))
        
        if from_location and to_location and from_location == to_location:
            flash('❌ From and To locations cannot be the same!', 'error')
            return redirect(url_for('add_movement'))
        
        movement_id = f"MOV{str(uuid.uuid4())[:6].upper()}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            conn.execute('''
                INSERT INTO product_movements (movement_id, timestamp, from_location, to_location, product_id, quantity, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (movement_id, timestamp, from_location, to_location, product_id, quantity, notes))
            conn.commit()
            flash('✅ Movement recorded successfully!', 'success')
            return redirect(url_for('movements_list'))
        except:
            flash('❌ Error recording movement!', 'error')
        finally:
            conn.close()
    
    products = conn.execute('SELECT * FROM products ORDER BY product_name').fetchall()
    locations = conn.execute('SELECT * FROM locations ORDER BY location_name').fetchall()
    conn.close()
    
    return render_template('movements/add.html', products=products, locations=locations)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        from_location = request.form['from_location'] if request.form['from_location'] != '' else None
        to_location = request.form['to_location'] if request.form['to_location'] != '' else None
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        notes = request.form.get('notes', '').strip()
        
        if not from_location and not to_location:
            flash('❌ Either From or To location must be specified!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if from_location and to_location and from_location == to_location:
            flash('❌ From and To locations cannot be the same!', 'error')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        try:
            conn.execute('''
                UPDATE product_movements 
                SET from_location = ?, to_location = ?, product_id = ?, quantity = ?, notes = ?
                WHERE movement_id = ?
            ''', (from_location, to_location, product_id, quantity, notes, movement_id))
            conn.commit()
            flash('✅ Movement updated successfully!', 'success')
            return redirect(url_for('movements_list'))
        except:
            flash('❌ Error updating movement!', 'error')
        finally:
            conn.close()
    
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
    
    products = conn.execute('SELECT * FROM products ORDER BY product_name').fetchall()
    locations = conn.execute('SELECT * FROM locations ORDER BY location_name').fetchall()
    conn.close()
    
    if not movement:
        flash('❌ Movement not found!', 'error')
        return redirect(url_for('movements_list'))
    
    return render_template('movements/edit.html', movement=movement, products=products, locations=locations)

# Report route
@app.route('/reports/inventory')
def inventory_report():
    conn = get_db_connection()
    
    report_data = conn.execute('''
        WITH incoming AS (
            SELECT product_id, to_location as location_id, SUM(quantity) as total_in
            FROM product_movements 
            WHERE to_location IS NOT NULL
            GROUP BY product_id, to_location
        ),
        outgoing AS (
            SELECT product_id, from_location as location_id, SUM(quantity) as total_out
            FROM product_movements 
            WHERE from_location IS NOT NULL
            GROUP BY product_id, from_location
        )
        SELECT 
            p.product_id,
            p.product_name,
            l.location_id,
            l.location_name,
            COALESCE(i.total_in, 0) - COALESCE(o.total_out, 0) as balance
        FROM products p
        CROSS JOIN locations l
        LEFT JOIN incoming i ON p.product_id = i.product_id AND l.location_id = i.location_id
        LEFT JOIN outgoing o ON p.product_id = o.product_id AND l.location_id = o.location_id
        WHERE COALESCE(i.total_in, 0) - COALESCE(o.total_out, 0) > 0
        ORDER BY p.product_name, l.location_name
    ''').fetchall()
    
    conn.close()
    return render_template('reports/inventory.html', report_data=report_data)

if __name__ == '__main__':
    print("🚀 Starting StockTrack Pro Server...")
    print("📊 Access your application at: http://localhost:5000")
    print("🛑 Press CTRL+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)