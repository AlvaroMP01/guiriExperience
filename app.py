from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DATABASE = 'guiriexperience.db'

# ==================== DATABASE FUNCTIONS ====================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tours table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            guide TEXT NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cruises table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cruises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            ship TEXT NOT NULL,
            departure_date DATE NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Buses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            price REAL NOT NULL,
            seats_available INTEGER DEFAULT 50,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Trains table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            price REAL NOT NULL,
            seats_available INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Reservations table (for statistics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_type TEXT NOT NULL,
            service_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM tours")
    if cursor.fetchone()[0] == 0:
        sample_tours = [
            ('Madrid City Tour', 'Cultural', 'Carlos García', '2024-03-15', '10:00', 45.00, 'Explore the historic center of Madrid'),
            ('Flamenco Experience', 'Cultural', 'María López', '2024-03-16', '20:00', 65.00, 'Authentic flamenco show with dinner'),
            ('Tapas & Wine Tour', 'Gastronomic', 'Juan Martínez', '2024-03-17', '19:00', 55.00, 'Taste the best tapas in town'),
        ]
        cursor.executemany(
            "INSERT INTO tours (name, category, guide, date, time, price, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            sample_tours
        )
    
    cursor.execute("SELECT COUNT(*) FROM cruises")
    if cursor.fetchone()[0] == 0:
        sample_cruises = [
            ('Mediterranean Paradise', 'Ocean Dream', '2024-04-10', 7, 899.00, 'Visit Greece, Italy, and Spain'),
            ('Caribbean Adventure', 'Sea Explorer', '2024-05-15', 10, 1299.00, 'Explore the Caribbean islands'),
        ]
        cursor.executemany(
            "INSERT INTO cruises (destination, ship, departure_date, duration, price, description) VALUES (?, ?, ?, ?, ?, ?)",
            sample_cruises
        )
    
    cursor.execute("SELECT COUNT(*) FROM buses")
    if cursor.fetchone()[0] == 0:
        sample_buses = [
            ('Madrid', 'Barcelona', '08:00', '14:30', 35.00, 50),
            ('Seville', 'Granada', '10:30', '13:45', 22.00, 50),
        ]
        cursor.executemany(
            "INSERT INTO buses (origin, destination, departure_time, arrival_time, price, seats_available) VALUES (?, ?, ?, ?, ?, ?)",
            sample_buses
        )
    
    cursor.execute("SELECT COUNT(*) FROM trains")
    if cursor.fetchone()[0] == 0:
        sample_trains = [
            ('Madrid', 'Valencia', '07:30', '09:25', 42.00, 100),
            ('Barcelona', 'Zaragoza', '15:00', '16:30', 28.00, 100),
        ]
        cursor.executemany(
            "INSERT INTO trains (origin, destination, departure_time, arrival_time, price, seats_available) VALUES (?, ?, ?, ?, ?, ?)",
            sample_trains
        )
    
    # Add some sample reservations for statistics
    cursor.execute("SELECT COUNT(*) FROM reservations")
    if cursor.fetchone()[0] == 0:
        sample_reservations = [
            ('tour', 1, 2, 90.00, 'CONFIRMED'),
            ('cruise', 1, 1, 899.00, 'CONFIRMED'),
            ('bus', 1, 3, 105.00, 'CONFIRMED'),
            ('train', 1, 2, 84.00, 'PENDING'),
        ]
        cursor.executemany(
            "INSERT INTO reservations (service_type, service_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
            sample_reservations
        )
    
    conn.commit()
    conn.close()

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/tours')
def tours():
    """Tours page"""
    conn = get_db()
    tours = conn.execute('SELECT * FROM tours ORDER BY date').fetchall()
    conn.close()
    return render_template('tours.html', tours=tours)

@app.route('/cruises')
def cruises():
    """Cruises page"""
    conn = get_db()
    cruises = conn.execute('SELECT * FROM cruises ORDER BY departure_date').fetchall()
    conn.close()
    return render_template('cruceros.html', cruises=cruises)

@app.route('/buses')
def buses():
    """Buses page"""
    conn = get_db()
    buses = conn.execute('SELECT * FROM buses ORDER BY departure_time').fetchall()
    conn.close()
    return render_template('bus.html', buses=buses)

@app.route('/trains')
def trains():
    """Trains page"""
    conn = get_db()
    trains = conn.execute('SELECT * FROM trains ORDER BY departure_time').fetchall()
    conn.close()
    return render_template('trenes.html', trains=trains)

@app.route('/reservations')
def reservations():
    """Reservations page - for now just shows the template"""
    return render_template('reservas.html', reservations=[])

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
def admin():
    """Admin panel - unified view"""
    conn = get_db()
    
    # Get all data
    tours = conn.execute('SELECT * FROM tours ORDER BY date').fetchall()
    cruises = conn.execute('SELECT * FROM cruises ORDER BY departure_date').fetchall()
    buses = conn.execute('SELECT * FROM buses ORDER BY departure_time').fetchall()
    trains = conn.execute('SELECT * FROM trains ORDER BY departure_time').fetchall()
    
    # Calculate statistics
    total_services = len(tours) + len(cruises) + len(buses) + len(trains)
    total_bookings = conn.execute('SELECT COUNT(*) FROM reservations').fetchone()[0]
    active_services = total_services  # For now, all are active
    total_revenue = conn.execute('SELECT SUM(total_price) FROM reservations').fetchone()[0] or 0
    
    conn.close()
    
    return render_template('admin.html',
                         tours=tours,
                         cruises=cruises,
                         buses=buses,
                         trains=trains,
                         total_services=total_services,
                         total_bookings=total_bookings,
                         active_services=active_services,
                         total_revenue=total_revenue)

# ==================== TOURS ADMIN ROUTES ====================

@app.route('/admin/tour/add', methods=['POST'])
def add_tour():
    """Add new tour"""
    name = request.form.get('name')
    category = request.form.get('category')
    guide = request.form.get('guide')
    date = request.form.get('date')
    time = request.form.get('time')
    price = request.form.get('price')
    
    conn = get_db()
    conn.execute(
        'INSERT INTO tours (name, category, guide, date, time, price) VALUES (?, ?, ?, ?, ?, ?)',
        (name, category, guide, date, time, price)
    )
    conn.commit()
    conn.close()
    
    flash('Tour added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/tour/<int:id>/delete', methods=['POST'])
def delete_tour(id):
    """Delete tour"""
    conn = get_db()
    conn.execute('DELETE FROM tours WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== CRUISES ADMIN ROUTES ====================

@app.route('/admin/cruise/add', methods=['POST'])
def add_cruise():
    """Add new cruise"""
    destination = request.form.get('destination')
    ship = request.form.get('ship')
    departure_date = request.form.get('departure_date')
    duration = request.form.get('duration')
    price = request.form.get('price')
    
    conn = get_db()
    conn.execute(
        'INSERT INTO cruises (destination, ship, departure_date, duration, price) VALUES (?, ?, ?, ?, ?)',
        (destination, ship, departure_date, duration, price)
    )
    conn.commit()
    conn.close()
    
    flash('Cruise added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/cruise/<int:id>/delete', methods=['POST'])
def delete_cruise(id):
    """Delete cruise"""
    conn = get_db()
    conn.execute('DELETE FROM cruises WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== BUSES ADMIN ROUTES ====================

@app.route('/admin/bus/add', methods=['POST'])
def add_bus_route():
    """Add new bus route"""
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    
    conn = get_db()
    conn.execute(
        'INSERT INTO buses (origin, destination, departure_time, arrival_time, price) VALUES (?, ?, ?, ?, ?)',
        (origin, destination, departure_time, arrival_time, price)
    )
    conn.commit()
    conn.close()
    
    flash('Bus route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/bus/<int:id>/delete', methods=['POST'])
def delete_bus(id):
    """Delete bus route"""
    conn = get_db()
    conn.execute('DELETE FROM buses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== TRAINS ADMIN ROUTES ====================

@app.route('/admin/train/add', methods=['POST'])
def add_train_route():
    """Add new train route"""
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    
    conn = get_db()
    conn.execute(
        'INSERT INTO trains (origin, destination, departure_time, arrival_time, price) VALUES (?, ?, ?, ?, ?)',
        (origin, destination, departure_time, arrival_time, price)
    )
    conn.commit()
    conn.close()
    
    flash('Train route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/train/<int:id>/delete', methods=['POST'])
def delete_train(id):
    """Delete train route"""
    conn = get_db()
    conn.execute('DELETE FROM trains WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== RUN APP ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
