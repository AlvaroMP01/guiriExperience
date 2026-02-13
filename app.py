from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import os
from models import db, Tour, Cruise, Bus, Train, Reservation, ExperienciaCulinaria, Hotel, CasaAlquiler, Reserva, Usuario

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guiriexperience.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize mechanisms
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Initialize sample data if needed (Logic from Group 1's init_db can be adapted here if desired, 
    # but for now we rely on db.create_all and manual addition or existing data)
    # Check if we need to seed Group 1 data
    if Tour.query.count() == 0:
        sample_tours = [
            Tour(name='Madrid City Tour', category='Cultural', guide='Carlos García', date='2024-03-15', time='10:00', price=45.00, description='Explore the historic center of Madrid'),
            Tour(name='Flamenco Experience', category='Cultural', guide='María López', date='2024-03-16', time='20:00', price=65.00, description='Authentic flamenco show with dinner'),
            Tour(name='Tapas & Wine Tour', category='Gastronomic', guide='Juan Martínez', date='2024-03-17', time='19:00', price=55.00, description='Taste the best tapas in town'),
        ]
        db.session.add_all(sample_tours)
        db.session.commit()
        
    if Cruise.query.count() == 0:
        sample_cruises = [
            Cruise(destination='Mediterranean Paradise', ship='Ocean Dream', departure_date='2024-04-10', duration=7, price=899.00, description='Visit Greece, Italy, and Spain'),
            Cruise(destination='Caribbean Adventure', ship='Sea Explorer', departure_date='2024-05-15', duration=10, price=1299.00, description='Explore the Caribbean islands'),
        ]
        db.session.add_all(sample_cruises)
        db.session.commit()

    if Bus.query.count() == 0:
        sample_buses = [
            Bus(origin='Madrid', destination='Barcelona', departure_time='08:00', arrival_time='14:30', price=35.00),
            Bus(origin='Seville', destination='Granada', departure_time='10:30', arrival_time='13:45', price=22.00),
        ]
        db.session.add_all(sample_buses)
        db.session.commit()

    if Train.query.count() == 0:
        sample_trains = [
            Train(origin='Madrid', destination='Valencia', departure_time='07:30', arrival_time='09:25', price=42.00),
            Train(origin='Barcelona', destination='Zaragoza', departure_time='15:00', arrival_time='16:30', price=28.00),
        ]
        db.session.add_all(sample_trains)
        db.session.commit()


# ==================== MAIN ROUTES (Group 1 & 2 Combined) ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# --- Group 1 Routes ---

@app.route('/tours')
def tours():
    """Tours page"""
    tours = Tour.query.order_by(Tour.date).all()
    return render_template('tours.html', tours=tours)

@app.route('/cruises')
def cruises():
    """Cruises page"""
    cruises = Cruise.query.order_by(Cruise.departure_date).all()
    return render_template('cruceros.html', cruises=cruises)

@app.route('/buses')
def buses():
    """Buses page"""
    buses = Bus.query.order_by(Bus.departure_time).all()
    return render_template('bus.html', buses=buses)

@app.route('/trains')
def trains():
    """Trains page"""
    trains = Train.query.order_by(Train.departure_time).all()
    return render_template('trenes.html', trains=trains)

@app.route('/reservations')
def reservations():
    """Reservations page (Group 1)"""
    # Fetch reservations with some details
    reservations_data = Reservation.query.order_by(Reservation.created_at.desc()).all()
    
    # Enrich data with service details
    reservations = []
    for res in reservations_data:
        res_dict = {
            'id': res.id,
            'service_type': res.service_type,
            'service_id': res.service_id,
            'quantity': res.quantity,
            'total_price': res.total_price,
            'status': res.status,
            'created_at': res.created_at
        }
        
        detail = "Servicio desconocido"
        if res.service_type == 'tour':
            item = Tour.query.get(res.service_id)
            if item: detail = f"Tour: {item.name}"
        elif res.service_type == 'cruise':
            item = Cruise.query.get(res.service_id)
            if item: detail = f"Crucero: {item.destination} ({item.ship})"
        elif res.service_type == 'bus':
            item = Bus.query.get(res.service_id)
            if item: detail = f"Bus: {item.origin} -> {item.destination}"
        elif res.service_type == 'train':
            item = Train.query.get(res.service_id)
            if item: detail = f"Tren: {item.origin} -> {item.destination}"
            
        res_dict['detail'] = detail
        reservations.append(res_dict)
        
    return render_template('reservas.html', reservations=reservations)

# --- Group 2 Routes ---

@app.route('/experiences')
def list_experiences():
    experiences = ExperienciaCulinaria.query.all()
    return render_template('experiences.html', experiences=experiences)

@app.route('/hotels')
def list_hotels():
    hotels = Hotel.query.all()
    return render_template('hotels.html', hotels=hotels)

@app.route('/houses')
def list_houses():
    houses = CasaAlquiler.query.all()
    return render_template('houses.html', houses=houses)

@app.route('/experience/<int:id>')
def experience_detail(id):
    service = ExperienciaCulinaria.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='experience')

@app.route('/hotel/<int:id>')
def hotel_detail(id):
    service = Hotel.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='hotel')

@app.route('/house/<int:id>')
def house_detail(id):
    service = CasaAlquiler.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='house')

@app.route('/checkout/<string:type>/<int:id>')
def checkout(type, id):
    if type == 'experience':
        service = ExperienciaCulinaria.query.get_or_404(id)
        price = service.precio
    elif type == 'hotel':
        service = Hotel.query.get_or_404(id)
        price = service.precio_noche
    elif type == 'house':
        service = CasaAlquiler.query.get_or_404(id)
        price = service.precio_dia
    else:
        return redirect(url_for('index'))
    
    date = request.args.get('date')
    quantity = int(request.args.get('quantity', 1))
    total = price * quantity
    
    return render_template('checkout.html', service=service, type=type, date=date, quantity=quantity, price=price, total=total)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Simulate payment processing
    # In a real app, integrate Stripe/PayPal here
    
    # Extract data from form
    service_id = request.form.get('service_id')
    service_type = request.form.get('type')
    date = request.form.get('date')
    quantity = request.form.get('quantity')
    total = request.form.get('total')
    
    # Store reservation (Linking to a dummy user for now since auth isn't fully active in this context)
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except:
        date_obj = datetime.now().date()
    
    # Need to check if user exists, if not create dummy
    user = Usuario.query.first()
    if not user:
        user = Usuario(username='demo_user', email='demo@example.com', password='password')
        db.session.add(user)
        db.session.commit()
        
    new_reservation = Reserva(
        usuario_id=user.id, 
        tipo_servicio=service_type, 
        servicio_id=int(service_id), 
        fecha_inicio=date_obj, 
        total=float(total), 
        estado='CONFIRMED'
    )
    db.session.add(new_reservation)
    db.session.commit()
    
    flash('Payment successful! Your booking is confirmed.', 'success')
    return redirect(url_for('index'))


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
def admin():
    """Admin panel - unified view (Group 1)"""
    
    # Get all data
    tours = Tour.query.order_by(Tour.date).all()
    cruises = Cruise.query.order_by(Cruise.departure_date).all()
    buses = Bus.query.order_by(Bus.departure_time).all()
    trains = Train.query.order_by(Train.departure_time).all()
    
    # Calculate statistics
    total_services = len(tours) + len(cruises) + len(buses) + len(trains)
    total_bookings = Reservation.query.count()
    active_services = total_services  # For now, all are active
    
    # Calculate revenue
    # SQLite doesn't return Decimal, simple sum in Python ok for small scale
    reservations = Reservation.query.all()
    total_revenue = sum(r.total_price for r in reservations)
    
    return render_template('admin.html',
                         tours=tours,
                         cruises=cruises,
                         buses=buses,
                         trains=trains,
                         total_services=total_services,
                         total_bookings=total_bookings,
                         active_services=active_services,
                         total_revenue=total_revenue)

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin Dashboard (Group 2)"""
    experiences = ExperienciaCulinaria.query.all()
    hotels = Hotel.query.all()
    houses = CasaAlquiler.query.all()
    reservations = Reserva.query.all()
    return render_template('admin/dashboard.html', 
                           experiences=experiences, 
                           hotels=hotels, 
                           houses=houses,
                           reservations=reservations)

# ==================== GROUP 1 ADMIN ACTIONS ====================

@app.route('/admin/tour/add', methods=['POST'])
def add_tour():
    name = request.form.get('name')
    category = request.form.get('category')
    guide = request.form.get('guide')
    date = request.form.get('date')
    time = request.form.get('time')
    price = request.form.get('price')
    
    new_tour = Tour(name=name, category=category, guide=guide, date=date, time=time, price=float(price))
    db.session.add(new_tour)
    db.session.commit()
    
    flash('Tour added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/tour/<int:id>/delete', methods=['POST'])
def delete_tour(id):
    tour = Tour.query.get(id)
    if tour:
        db.session.delete(tour)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/cruise/add', methods=['POST'])
def add_cruise():
    destination = request.form.get('destination')
    ship = request.form.get('ship')
    departure_date = request.form.get('departure_date')
    duration = request.form.get('duration')
    price = request.form.get('price')
    
    new_cruise = Cruise(destination=destination, ship=ship, departure_date=departure_date, duration=int(duration), price=float(price))
    db.session.add(new_cruise)
    db.session.commit()
    
    flash('Cruise added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/cruise/<int:id>/delete', methods=['POST'])
def delete_cruise(id):
    cruise = Cruise.query.get(id)
    if cruise:
        db.session.delete(cruise)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/bus/add', methods=['POST'])
def add_bus_route():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    
    new_bus = Bus(origin=origin, destination=destination, departure_time=departure_time, arrival_time=arrival_time, price=float(price))
    db.session.add(new_bus)
    db.session.commit()
    
    flash('Bus route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/bus/<int:id>/delete', methods=['POST'])
def delete_bus(id):
    bus = Bus.query.get(id)
    if bus:
        db.session.delete(bus)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/train/add', methods=['POST'])
def add_train_route():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')
    
    new_train = Train(origin=origin, destination=destination, departure_time=departure_time, arrival_time=arrival_time, price=float(price))
    db.session.add(new_train)
    db.session.commit()
    
    flash('Train route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/train/<int:id>/delete', methods=['POST'])
def delete_train(id):
    train = Train.query.get(id)
    if train:
        db.session.delete(train)
        db.session.commit()
    return jsonify({'success': True})

# ==================== GROUP 1 BOOKING ACTIONS ====================

@app.route('/book/tour', methods=['POST'])
def book_tour():
    tour_id = request.form.get('tour_id')
    quantity = request.form.get('quantity', 1)
    
    tour = Tour.query.get(tour_id)
    if tour:
        total_price = tour.price * int(quantity)
        new_res = Reservation(service_type='tour', service_id=tour.id, quantity=int(quantity), total_price=total_price, status='CONFIRMED')
        db.session.add(new_res)
        db.session.commit()
        flash('¡Tour reservado con éxito!', 'success')
    else:
        flash('Error: Tour no encontrado.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/cruise', methods=['POST'])
def book_cruise():
    cruise_id = request.form.get('cruise_id')
    passengers = request.form.get('passengers', 1)
    cabin_type = request.form.get('cabin_type', 'interior')
    
    cruise = Cruise.query.get(cruise_id)
    if cruise:
        base_price = cruise.price
        extra = 0
        if cabin_type == 'exterior': extra = 100
        elif cabin_type == 'balcony': extra = 250
        elif cabin_type == 'suite': extra = 500
        
        total_price = (base_price + extra) * int(passengers)
        
        new_res = Reservation(service_type='cruise', service_id=cruise.id, quantity=int(passengers), total_price=total_price, status='CONFIRMED')
        db.session.add(new_res)
        db.session.commit()
        flash('¡Crucero reservado con éxito!', 'success')
    else:
        flash('Error: Crucero no encontrado.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/bus', methods=['POST'])
def book_bus_ticket():
    bus_id = request.form.get('bus_id')
    quantity = request.form.get('quantity', 1)
    
    bus = Bus.query.get(bus_id)
    if bus:
        total_price = bus.price * int(quantity)
        new_res = Reservation(service_type='bus', service_id=bus.id, quantity=int(quantity), total_price=total_price, status='CONFIRMED')
        db.session.add(new_res)
        db.session.commit()
        flash('¡Billete de autobús reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de autobús no encontrada.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/train', methods=['POST'])
def book_train_ticket():
    train_id = request.form.get('train_id')
    quantity = request.form.get('quantity', 1)
    train_class = request.form.get('class', 'tourist')
    
    train = Train.query.get(train_id)
    if train:
        base_price = train.price
        extra = 0
        if train_class == 'tourist_plus': extra = 15
        elif train_class == 'preferente': extra = 30
        
        total_price = (base_price + extra) * int(quantity)
        
        new_res = Reservation(service_type='train', service_id=train.id, quantity=int(quantity), total_price=total_price, status='CONFIRMED')
        db.session.add(new_res)
        db.session.commit()
        flash('¡Billete de tren reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de tren no encontrada.', 'error')
    
    return redirect(url_for('reservations'))


# ==================== GROUP 2 ADMIN ACTIONS ====================

@app.route('/admin/add/<string:service_type>', methods=['GET', 'POST'])
def add_service(service_type):
    if request.method == 'POST':
        # Ensure dummy user exists for provider_id
        user = Usuario.query.first()
        if not user:
            user = Usuario(username='admin', email='admin@example.com', password='admin', role='ADMIN')
            db.session.add(user)
            db.session.commit()
            
        if service_type == 'experience':
            new_item = ExperienciaCulinaria(
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'], 
                proveedor_id=user.id
            )
        elif service_type == 'hotel':
            new_item = Hotel(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                estrellas=int(request.form['estrellas']),
                precio_noche=float(request.form['precio_noche']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=user.id
            )
        elif service_type == 'house':
            new_item = CasaAlquiler(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                habitaciones=int(request.form['habitaciones']),
                precio_dia=float(request.form['precio_dia']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=user.id
            )
        
        db.session.add(new_item)
        db.session.commit()
        flash(f'{service_type.capitalize()} added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/service_form.html', action='Add', type=service_type)

@app.route('/admin/edit/<string:service_type>/<int:id>', methods=['GET', 'POST'])
def edit_service(service_type, id):
    if service_type == 'experience':
        item = ExperienciaCulinaria.query.get_or_404(id)
    elif service_type == 'hotel':
        item = Hotel.query.get_or_404(id)
    elif service_type == 'house':
        item = CasaAlquiler.query.get_or_404(id)
    
    if request.method == 'POST':
        if service_type == 'experience':
            item.titulo = request.form['titulo']
            item.descripcion = request.form['descripcion']
            item.precio = float(request.form['precio'])
            item.ubicacion = request.form['ubicacion']
            item.imagen = request.form['imagen']
        elif service_type == 'hotel':
            item.nombre = request.form['nombre']
            item.descripcion = request.form['descripcion']
            item.estrellas = int(request.form['estrellas'])
            item.precio_noche = float(request.form['precio_noche'])
            item.ubicacion = request.form['ubicacion']
            item.imagen = request.form['imagen']
        elif service_type == 'house':
            item.nombre = request.form['nombre']
            item.descripcion = request.form['descripcion']
            item.habitaciones = int(request.form['habitaciones'])
            item.precio_dia = float(request.form['precio_dia'])
            item.ubicacion = request.form['ubicacion']
            item.imagen = request.form['imagen']
        
        db.session.commit()
        flash(f'{service_type.capitalize()} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/service_form.html', action='Edit', type=service_type, item=item)

@app.route('/admin/delete/<string:service_type>/<int:id>')
def delete_service(service_type, id):
    if service_type == 'experience':
        item = ExperienciaCulinaria.query.get_or_404(id)
    elif service_type == 'hotel':
        item = Hotel.query.get_or_404(id)
    elif service_type == 'house':
        item = CasaAlquiler.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()
    flash(f'{service_type.capitalize()} deleted successfully!', 'danger')
    return redirect(url_for('admin_dashboard'))

# ==================== MOCK AUTH ROUTES ====================

@app.route('/login')
def login():
    """Mock login"""
    session['user_id'] = 1
    session['role'] = 'ADMIN' 
    flash('Has iniciado sesión (Mock)', 'info')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Mock logout"""
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    """Mock register"""
    return redirect(url_for('login'))


if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        try:
            os.makedirs('static/uploads')
        except:
            pass
    app.run(debug=True, host='0.0.0.0', port=5000)
