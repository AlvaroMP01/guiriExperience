from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, ExperienciaCulinaria, Hotel, CasaAlquiler, Reserva, Usuario
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'group_2_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

# Create database if it doesn't exist
with app.app_context():
    db.create_all()
    # Sample data could be inserted here

@app.route('/')
def index():
    return render_template('index.html')

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
    service_id = request.form['service_id']
    service_type = request.form['type']
    date = request.form['date']
    quantity = request.form['quantity']
    total = request.form['total']
    
    # Store reservation (Linking to a dummy user for now since auth isn't fully active in this context)
    # Convert string date to date object
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

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    experiences = ExperienciaCulinaria.query.all()
    hotels = Hotel.query.all()
    houses = CasaAlquiler.query.all()
    reservations = Reserva.query.all()
    return render_template('admin/dashboard.html', 
                           experiences=experiences, 
                           hotels=hotels, 
                           houses=houses,
                           reservations=reservations)

@app.route('/admin/add/<string:service_type>', methods=['GET', 'POST'])
def add_service(service_type):
    if request.method == 'POST':
        if service_type == 'experience':
            new_item = ExperienciaCulinaria(
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                ubicacion=request.form['ubicacion'],
                imagen=request.form['imagen'], # Simplified for now, should handle file upload
                proveedor_id=1 # Hardcoded for now
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

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(debug=True)
