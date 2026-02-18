from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Tour, Cruise, Bus, Train, Reservation, ExperienciaCulinaria, Hotel, CasaAlquiler, Reserva, User

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guiriexperience.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize mechanisms
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context Processor to inject user into templates
@app.context_processor
def inject_user():
    return dict(user=current_user)

# Helper to sync session for legacy compatibility (Group 1 code uses session['role'])
@app.before_request
def sync_session_legacy():
    if current_user.is_authenticated:
        session['user_id'] = current_user.id
        session['role'] = current_user.role

# Create database tables
with app.app_context():
    db.create_all()
    
    # Initialize sample data if needed
    if Tour.query.count() == 0:
        sample_tours = [
            Tour(name='Madrid City Tour', category='Cultural', guide='Carlos García', date='2024-03-15', time='10:00', price=45.00, description='Explore the historic center of Madrid'),
            Tour(name='Flamenco Experience', category='Cultural', guide='María López', date='2024-03-16', time='20:00', price=65.00, description='Authentic flamenco show with dinner'),
            Tour(name='Tapas & Wine Tour', category='Gastronomic', guide='Juan Martínez', date='2024-03-17', time='19:00', price=55.00, description='Taste the best tapas in town'),
        ]
        db.session.add_all(sample_tours)
        db.session.commit()
    
    # Ensure default admin exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', password=generate_password_hash('admin123'), role='ADMIN')
        db.session.add(admin)
        db.session.commit()

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# --- Group 1 Routes ---

@app.route('/tours')
def tours():
    tours = Tour.query.order_by(Tour.date).all()
    return render_template('tours.html', tours=tours)

@app.route('/cruises')
def cruises():
    cruises = Cruise.query.order_by(Cruise.departure_date).all()
    return render_template('cruceros.html', cruises=cruises)

@app.route('/buses')
def buses():
    buses = Bus.query.order_by(Bus.departure_time).all()
    return render_template('bus.html', buses=buses)

@app.route('/trains')
def trains():
    trains = Train.query.order_by(Train.departure_time).all()
    return render_template('trenes.html', trains=trains)

@app.route('/reservations')
@login_required
def reservations():
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
@login_required
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
@login_required
def process_payment():
    service_id = request.form.get('service_id')
    service_type = request.form.get('type')
    date = request.form.get('date')
    total = request.form.get('total')
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except:
        date_obj = datetime.now().date()
    
    new_reservation = Reserva(
        usuario_id=current_user.id, 
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
@login_required
def admin():
    if current_user.role not in ['ADMIN', 'TOUR_SELLER', 'CRUISE_SELLER', 'BUS_SELLER', 'TRAIN_SELLER']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
        
    tours = Tour.query.order_by(Tour.date).all()
    cruises = Cruise.query.order_by(Cruise.departure_date).all()
    buses = Bus.query.order_by(Bus.departure_time).all()
    trains = Train.query.order_by(Train.departure_time).all()
    
    total_services = len(tours) + len(cruises) + len(buses) + len(trains)
    total_bookings = Reservation.query.count()
    reservations = Reservation.query.all()
    total_revenue = sum(r.total_price for r in reservations)
    
    return render_template('admin.html',
                         tours=tours,
                         cruises=cruises,
                         buses=buses,
                         trains=trains,
                         total_services=total_services,
                         total_bookings=total_bookings,
                         active_services=total_services,
                         total_revenue=total_revenue)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role not in ['ADMIN', 'PROVIDER']: # Assuming PROVIDER role exists for Group 2
        flash('Access denied', 'error')
        return redirect(url_for('index'))
        
    experiences = ExperienciaCulinaria.query.all()
    hotels = Hotel.query.all()
    houses = CasaAlquiler.query.all()
    reservations = Reserva.query.all()
    return render_template('admin/dashboard.html', 
                           experiences=experiences, 
                           hotels=hotels, 
                           houses=houses,
                           reservations=reservations)

# ==================== GROUP 3 ADMIN ACTIONS (USER MANAGEMENT) ====================

@app.route('/admin/users')
@login_required
def user_dashboard():
    if current_user.role not in ['ADMIN', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role not in ['ADMIN', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully', 'success')
            return redirect(url_for('user_dashboard'))
            
    return render_template('admin_user_form.html', action='Create')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role not in ['ADMIN', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        
        if request.form.get('password'):
            user.password = generate_password_hash(request.form.get('password'))
            
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user_dashboard'))
        
    return render_template('admin_user_form.html', action='Edit', user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role not in ['ADMIN', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id: # Prevent self-deletion
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    else:
        flash('Cannot delete yourself', 'error')
        
    return redirect(url_for('user_dashboard'))


# ==================== GROUP 1 ADMIN ACTIONS ====================
# (Kept separate for simplicity, could be unified with decorators)

@app.route('/admin/tour/add', methods=['POST'])
@login_required
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
@login_required
def delete_tour(id):
    tour = Tour.query.get(id)
    if tour:
        db.session.delete(tour)
        db.session.commit()
    return jsonify({'success': True})

# ... Similar updates for Cruise, Bus, Train add/delete (adding @login_required)
# For brevity, I'm skipping explicit re-writing of ALL identical boilerplate but I MUST write the full file content.
# I will include them.

@app.route('/admin/cruise/add', methods=['POST'])
@login_required
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
@login_required
def delete_cruise(id):
    cruise = Cruise.query.get(id)
    if cruise:
        db.session.delete(cruise)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/bus/add', methods=['POST'])
@login_required
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
@login_required
def delete_bus(id):
    bus = Bus.query.get(id)
    if bus:
        db.session.delete(bus)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/train/add', methods=['POST'])
@login_required
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
@login_required
def delete_train(id):
    train = Train.query.get(id)
    if train:
        db.session.delete(train)
        db.session.commit()
    return jsonify({'success': True})

# ==================== GROUP 1 BOOKING ACTIONS ====================

@app.route('/book/tour', methods=['POST'])
@login_required
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
    else: flash('Error: Tour no encontrado.', 'error')
    return redirect(url_for('reservations'))

@app.route('/book/cruise', methods=['POST'])
@login_required
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
    else: flash('Error: Crucero no encontrado.', 'error')
    return redirect(url_for('reservations'))

@app.route('/book/bus', methods=['POST'])
@login_required
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
    else: flash('Error: Ruta de autobús no encontrada.', 'error')
    return redirect(url_for('reservations'))

@app.route('/book/train', methods=['POST'])
@login_required
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
    else: flash('Error: Ruta de tren no encontrada.', 'error')
    return redirect(url_for('reservations'))

# ==================== GROUP 2 ADMIN ACTIONS ====================

@app.route('/admin/add/<string:service_type>', methods=['GET', 'POST'])
@login_required
def add_service(service_type):
    if request.method == 'POST':
        if service_type == 'experience':
            new_item = ExperienciaCulinaria(
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'], 
                proveedor_id=current_user.id
            )
        elif service_type == 'hotel':
            new_item = Hotel(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                estrellas=int(request.form['estrellas']),
                precio_noche=float(request.form['precio_noche']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=current_user.id
            )
        elif service_type == 'house':
            new_item = CasaAlquiler(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                habitaciones=int(request.form['habitaciones']),
                precio_dia=float(request.form['precio_dia']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'],
                proveedor_id=current_user.id
            )
        db.session.add(new_item)
        db.session.commit()
        flash(f'{service_type.capitalize()} added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/service_form.html', action='Add', type=service_type)

@app.route('/admin/edit/<string:service_type>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_type, id):
    if service_type == 'experience': item = ExperienciaCulinaria.query.get_or_404(id)
    elif service_type == 'hotel': item = Hotel.query.get_or_404(id)
    elif service_type == 'house': item = CasaAlquiler.query.get_or_404(id)
    
    if request.method == 'POST':
        # ... (Same logic as before, assumed simple field updates)
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
@login_required
def delete_service_g2(service_type, id):
    if service_type == 'experience': item = ExperienciaCulinaria.query.get_or_404(id)
    elif service_type == 'hotel': item = Hotel.query.get_or_404(id)
    elif service_type == 'house': item = CasaAlquiler.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f'{service_type.capitalize()} deleted successfully!', 'danger')
    return redirect(url_for('admin_dashboard'))

# ==================== AUTH ROUTES (Group 3) ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'USER') 
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or email already exists', 'error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('perfil.html', user=current_user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        if 'password' in request.form and request.form['password']:
            current_user.password = generate_password_hash(request.form['password'])
            db.session.commit()
            flash('Password updated', 'success')
    return render_template('editar_perfil.html', user=current_user)


if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        try: os.makedirs('static/uploads')
        except: pass
    app.run(debug=True, host='0.0.0.0', port=5000)
