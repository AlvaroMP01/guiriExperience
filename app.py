from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, User, Tour, Cruise, Bus, Train, Reservation, Usuario, ExperienciaCulinaria, Hotel, CasaAlquiler, Reserva
from datetime import datetime
import os

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database and tables
with app.app_context():
    db.create_all()
    print("✓ Database tables created/verified")
    
    # Insert sample data if tables are empty (Grupo1 data)
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

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Home page - accessible without login"""
    return render_template('index.html', user=current_user if current_user.is_authenticated else None)

@app.route('/home')
def home():
    """Alternative home route (Grupo3 style)"""
    return render_template('home.html', user=current_user if current_user.is_authenticated else None)

# ==================== AUTHENTICATION ROUTES (Grupo3) ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'usuario')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='El usuario ya existe')
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - redirects based on role"""
    is_admin_users = current_user.role == 'ADMIN1'
    is_admin_experiencias = current_user.role == 'ADMIN2'
    is_admin_tours = current_user.role == 'ADMIN3'

    if is_admin_users:
        return redirect(url_for('admin_dashboard_users'))
    elif is_admin_experiencias:
        return redirect(url_for('admin_dashboard'))
    elif is_admin_tours:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    """User profile page"""
    return render_template('perfil.html', user=current_user)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    """Edit user profile"""
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if new_password == confirm_password:
                current_user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Contraseña actualizada exitosamente', 'success')
                return redirect(url_for('perfil'))
            else:
                flash('Las contraseñas no coinciden', 'error')
        
    return render_template('editar_perfil.html', user=current_user)

# ==================== ADMIN USERS ROUTES (Grupo3) ====================

@app.route('/admin/users')
@login_required
def admin_dashboard_users():
    """Admin dashboard for user management"""
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado. Se requieren permisos de administrador de usuarios.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create new user"""
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'error')
            return render_template('admin_user_form.html', title='Crear Usuario')
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('admin_dashboard_users'))
        
    return render_template('admin_user_form.html', title='Crear Usuario')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit existing user"""
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        
        if password:
            user.password = generate_password_hash(password)
            
        user.role = role
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('admin_dashboard_users'))
        
    return render_template('admin_user_form.html', title='Editar Usuario', user=user)

@app.route('/admin/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    """Delete user"""
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario.', 'error')
        return redirect(url_for('admin_dashboard_users'))
        
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard_users'))

# ==================== GRUPO1 ROUTES (Tours, Cruises, Buses, Trains) ====================

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
    """Reservations page (Grupo1 style)"""
    reservations_data = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('reservas.html', reservations=reservations_data)

# ==================== GRUPO2 ROUTES (Experiences, Hotels, Houses) ====================

@app.route('/experiences')
def list_experiences():
    """Culinary experiences page"""
    experiences = ExperienciaCulinaria.query.all()
    return render_template('experiences.html', experiences=experiences)

@app.route('/hotels')
def list_hotels():
    """Hotels page"""
    hotels = Hotel.query.all()
    return render_template('hotels.html', hotels=hotels)

@app.route('/houses')
def list_houses():
    """Rental houses page"""
    houses = CasaAlquiler.query.all()
    return render_template('houses.html', houses=houses)

@app.route('/experience/<int:id>')
def experience_detail(id):
    """Experience detail page"""
    service = ExperienciaCulinaria.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='experience')

@app.route('/hotel/<int:id>')
def hotel_detail(id):
    """Hotel detail page"""
    service = Hotel.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='hotel')

@app.route('/house/<int:id>')
def house_detail(id):
    """House detail page"""
    service = CasaAlquiler.query.get_or_404(id)
    return render_template('service_detail.html', service=service, type='house')

@app.route('/checkout/<string:type>/<int:id>')
def checkout(type, id):
    """Checkout page (Grupo2 style)"""
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
    """Process payment (Grupo2 style)"""
    service_id = request.form['service_id']
    service_type = request.form['type']
    date = request.form['date']
    quantity = request.form['quantity']
    total = request.form['total']
    
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    
    new_reservation = Reserva(
        usuario_id=1, 
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
    """Admin panel - unified view (Grupo1 style)"""
    tours = Tour.query.order_by(Tour.date).all()
    cruises = Cruise.query.order_by(Cruise.departure_date).all()
    buses = Bus.query.order_by(Bus.departure_time).all()
    trains = Train.query.order_by(Train.departure_time).all()
    
    total_services = len(tours) + len(cruises) + len(buses) + len(trains)
    total_bookings = Reservation.query.count()
    active_services = total_services
    total_revenue = db.session.query(db.func.sum(Reservation.total_price)).scalar() or 0
    
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
    """Admin dashboard (Grupo2 style)"""
    experiences = ExperienciaCulinaria.query.all()
    hotels = Hotel.query.all()
    houses = CasaAlquiler.query.all()
    reservations = Reserva.query.all()
    return render_template('admin/dashboard.html', 
                           experiences=experiences, 
                           hotels=hotels, 
                           houses=houses,
                           reservations=reservations)

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
    
    new_tour = Tour(name=name, category=category, guide=guide, date=date, time=time, price=price)
    db.session.add(new_tour)
    db.session.commit()
    
    flash('Tour added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/tour/<int:id>/delete', methods=['POST'])
def delete_tour(id):
    """Delete tour"""
    tour = Tour.query.get_or_404(id)
    db.session.delete(tour)
    db.session.commit()
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
    
    new_cruise = Cruise(destination=destination, ship=ship, departure_date=departure_date, duration=duration, price=price)
    db.session.add(new_cruise)
    db.session.commit()
    
    flash('Cruise added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/cruise/<int:id>/delete', methods=['POST'])
def delete_cruise(id):
    """Delete cruise"""
    cruise = Cruise.query.get_or_404(id)
    db.session.delete(cruise)
    db.session.commit()
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
    
    new_bus = Bus(origin=origin, destination=destination, departure_time=departure_time, arrival_time=arrival_time, price=price)
    db.session.add(new_bus)
    db.session.commit()
    
    flash('Bus route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/bus/<int:id>/delete', methods=['POST'])
def delete_bus(id):
    """Delete bus route"""
    bus = Bus.query.get_or_404(id)
    db.session.delete(bus)
    db.session.commit()
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
    
    new_train = Train(origin=origin, destination=destination, departure_time=departure_time, arrival_time=arrival_time, price=price)
    db.session.add(new_train)
    db.session.commit()
    
    flash('Train route added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/train/<int:id>/delete', methods=['POST'])
def delete_train(id):
    """Delete train route"""
    train = Train.query.get_or_404(id)
    db.session.delete(train)
    db.session.commit()
    return jsonify({'success': True})

# ==================== GRUPO2 ADMIN ROUTES ====================

@app.route('/admin/add/<string:service_type>', methods=['GET', 'POST'])
def add_service(service_type):
    """Add service (Grupo2 style)"""
    if request.method == 'POST':
        if service_type == 'experience':
            new_item = ExperienciaCulinaria(
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=1
            )
        elif service_type == 'hotel':
            new_item = Hotel(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                estrellas=int(request.form['estrellas']),
                precio_noche=float(request.form['precio_noche']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=1
            )
        elif service_type == 'house':
            new_item = CasaAlquiler(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                habitaciones=int(request.form['habitaciones']),
                precio_dia=float(request.form['precio_dia']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=1
            )
        
        db.session.add(new_item)
        db.session.commit()
        flash(f'{service_type.capitalize()} added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/service_form.html', action='Add', type=service_type)

@app.route('/admin/edit/<string:service_type>/<int:id>', methods=['GET', 'POST'])
def edit_service(service_type, id):
    """Edit service (Grupo2 style)"""
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
    """Delete service (Grupo2 style)"""
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

# ==================== BOOKING ROUTES (Grupo1 style) ====================

@app.route('/book/tour', methods=['POST'])
def book_tour():
    """Book a tour"""
    tour_id = request.form.get('tour_id')
    quantity = request.form.get('quantity', 1)
    
    tour = Tour.query.get(tour_id)
    if tour:
        total_price = tour.price * int(quantity)
        new_reservation = Reservation(
            user_id=1,
            service_type='tour',
            service_id=tour_id,
            quantity=quantity,
            total_price=total_price,
            status='CONFIRMED'
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Tour reservado con éxito!', 'success')
    else:
        flash('Error: Tour no encontrado.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/cruise', methods=['POST'])
def book_cruise():
    """Book a cruise"""
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
        
        new_reservation = Reservation(
            user_id=1,
            service_type='cruise',
            service_id=cruise_id,
            quantity=passengers,
            total_price=total_price,
            status='CONFIRMED'
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Crucero reservado con éxito!', 'success')
    else:
        flash('Error: Crucero no encontrado.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/bus', methods=['POST'])
def book_bus_ticket():
    """Book a bus ticket"""
    bus_id = request.form.get('bus_id')
    quantity = request.form.get('quantity', 1)
    
    bus = Bus.query.get(bus_id)
    if bus:
        total_price = bus.price * int(quantity)
        new_reservation = Reservation(
            user_id=1,
            service_type='bus',
            service_id=bus_id,
            quantity=quantity,
            total_price=total_price,
            status='CONFIRMED'
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Billete de autobús reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de autobús no encontrada.', 'error')
    
    return redirect(url_for('reservations'))

@app.route('/book/train', methods=['POST'])
def book_train_ticket():
    """Book a train ticket"""
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
        
        new_reservation = Reservation(
            user_id=1,
            service_type='train',
            service_id=train_id,
            quantity=quantity,
            total_price=total_price,
            status='CONFIRMED'
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash('¡Billete de tren reservado con éxito!', 'success')
    else:
        flash('Error: Ruta de tren no encontrada.', 'error')
    
    return redirect(url_for('reservations'))

# ==================== RUN APP ====================

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True, host='0.0.0.0', port=5000)
