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
    """Reservations page"""
    conn = get_db()
    # Fetch reservations with some details (simplified for now)
    reservations_data = conn.execute('SELECT * FROM reservations ORDER BY created_at DESC').fetchall()
    
    # Enrich data with service details manually since we have separate tables
    reservations = []
    for res in reservations_data:
        res_dict = dict(res)
        service_id = res['service_id']
        service_type = res['service_type']
        
        detail = "Servicio desconocido"
        if service_type == 'tour':
            item = conn.execute('SELECT name FROM tours WHERE id = ?', (service_id,)).fetchone()
            if item: detail = f"Tour: {item['name']}"
        elif service_type == 'cruise':
            item = conn.execute('SELECT destination, ship FROM cruises WHERE id = ?', (service_id,)).fetchone()
            if item: detail = f"Crucero: {item['destination']} ({item['ship']})"
        elif service_type == 'bus':
            item = conn.execute('SELECT origin, destination FROM buses WHERE id = ?', (service_id,)).fetchone()
            if item: detail = f"Bus: {item['origin']} -> {item['destination']}"
        elif service_type == 'train':
            item = conn.execute('SELECT origin, destination FROM trains WHERE id = ?', (service_id,)).fetchone()
            if item: detail = f"Tren: {item['origin']} -> {item['destination']}"
            
        res_dict['detail'] = detail
        reservations.append(res_dict)
        
    conn.close()
    return render_template('reservas.html', reservations=reservations)

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

# ==================== BOOKING ROUTES ====================

@app.route('/book/tour', methods=['POST'])
def book_tour():
    """Book a tour"""
    tour_id = request.form.get('tour_id')
    # Default values for now, as the form might be simple
    quantity = request.form.get('quantity', 1)
    
    conn = get_db()
    # Get tour price
    tour = conn.execute('SELECT price FROM tours WHERE id = ?', (tour_id,)).fetchone()
    if tour:
        total_price = tour['price'] * int(quantity)
        conn.execute(
            "INSERT INTO reservations (service_type, service_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
            ('tour', tour_id, quantity, total_price, 'CONFIRMED')
        )
        conn.commit()
        flash('¡Tour reservado con éxito!', 'success')
    else:
        flash('Error: Tour no encontrado.', 'error')
    conn.close()
    
    return redirect(url_for('reservations'))

@app.route('/book/cruise', methods=['POST'])
def book_cruise():
    """Book a cruise"""
    cruise_id = request.form.get('cruise_id')
    passengers = request.form.get('passengers', 1)
    cabin_type = request.form.get('cabin_type', 'interior')
    
    conn = get_db()
    cruise = conn.execute('SELECT price FROM cruises WHERE id = ?', (cruise_id,)).fetchone()
    if cruise:
        # Simple price calculation logic
        base_price = cruise['price']
        extra = 0
        if cabin_type == 'exterior': extra = 100
        elif cabin_type == 'balcony': extra = 250
        elif cabin_type == 'suite': extra = 500
        
        total_price = (base_price + extra) * int(passengers)
        
        conn.execute(
            "INSERT INTO reservations (service_type, service_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
            ('cruise', cruise_id, passengers, total_price, 'CONFIRMED')
        )
        conn.commit()
        flash('¡Crucero reservado con éxito!', 'success')
    else:
        flash('Error: Crucero no encontrado.', 'error')
    conn.close()
    
    return redirect(url_for('reservations'))

@app.route('/book/bus', methods=['POST'])
def book_bus_ticket():
    """Book a bus ticket"""
    bus_id = request.form.get('bus_id')
    quantity = request.form.get('quantity', 1)
    
    conn = get_db()
    bus = conn.execute('SELECT price FROM buses WHERE id = ?', (bus_id,)).fetchone()
    if bus:
        total_price = bus['price'] * int(quantity)
        conn.execute(
            "INSERT INTO reservations (service_type, service_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
            ('bus', bus_id, quantity, total_price, 'CONFIRMED')
        )
        conn.commit()
        flash('¡Billete de autobús reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de autobús no encontrada.', 'error')
    conn.close()
    
    return redirect(url_for('reservations'))

@app.route('/book/train', methods=['POST'])
def book_train_ticket():
    """Book a train ticket"""
    train_id = request.form.get('train_id')
    quantity = request.form.get('quantity', 1)
    train_class = request.form.get('class', 'tourist')
    
    conn = get_db()
    train = conn.execute('SELECT price FROM trains WHERE id = ?', (train_id,)).fetchone()
    if train:
        base_price = train['price']
        extra = 0
        if train_class == 'tourist_plus': extra = 15
        elif train_class == 'preferente': extra = 30
        
        total_price = (base_price + extra) * int(quantity)
        
        conn.execute(
            "INSERT INTO reservations (service_type, service_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
            ('train', train_id, quantity, total_price, 'CONFIRMED')
        )
        conn.commit()
        flash('¡Billete de tren reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de tren no encontrada.', 'error')
    conn.close()
    
    return redirect(url_for('reservations'))

# ==================== MOCK AUTH ROUTES ====================
# These are placeholders so the buttons work. The other group will implement real auth.

@app.route('/login')
def login():
    """Mock login"""
    from flask import session
    session['user_id'] = 1
    session['role'] = 'ADMIN' # Default to ADMIN for easy testing
    flash('Has iniciado sesión (Mock)', 'info')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Mock logout"""
    from flask import session
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    """Mock register"""
    return redirect(url_for('login'))

# ==================== ADMIN ROUTES (Existing) ====================

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
