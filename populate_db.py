from app import app, db
from models import User, Tour, Cruise, Bus, Train, ExperienciaCulinaria, Hotel, CasaAlquiler, Reservation, Reserva
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def populate_db():
    with app.app_context():
        print("Creating all tables...")
        db.create_all()

        print("Populating Users...")
        # Create Users
        users_data = [
            ('admin', 'admin@guiri.com', 'admin123', 'ADMIN'),
            ('provider1', 'provider1@guiri.com', 'provider123', 'PROVIDER'),
            ('provider2', 'provider2@guiri.com', 'provider123', 'PROVIDER'),
            ('user1', 'user1@guiri.com', 'user123', 'USER'),
            ('user2', 'user2@guiri.com', 'user123', 'USER'),
            ('tour_seller', 'tours@guiri.com', 'seller123', 'TOUR_SELLER'),
        ]

        created_users = {}
        for username, email, password, role in users_data:
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(username=username, email=email, password=generate_password_hash(password), role=role)
                db.session.add(user)
                print(f"User {username} created.")
            else:
                print(f"User {username} already exists.")
            created_users[username] = user # This might be detached if not committed, but we commit at end or here? 
                                           # Better confirm persistence before using ID.
        
        db.session.commit()
        # Refetch to get IDs
        admin = User.query.filter_by(username='admin').first()
        provider1 = User.query.filter_by(username='provider1').first()
        
        print("Populating Group 1 Services (Tours, Cruises, etc.)...")
        # Tours
        if Tour.query.count() == 0:
            toursData = [
                Tour(name='Madrid Histórico', category='Cultural', guide='Juan Perez', date='2024-06-15', time='10:00', price=25.0, description='Recorrido por el Madrid de los Austrias.'),
                Tour(name='Ruta de Tapas', category='Gastronomía', guide='Maria Garcia', date='2024-06-16', time='20:00', price=45.0, description='Las mejores tapas de La Latina.'),
                Tour(name='Museo del Prado', category='Arte', guide='Carlos Ruiz', date='2024-06-17', time='11:00', price=30.0, description='Visita guiada a las obras maestras.'),
                Tour(name='Toledo de Noche', category='Aventura', guide='Ana Lopez', date='2024-06-18', time='21:00', price=35.0, description='Misterios y leyendas de Toledo.'),
                Tour(name='Segovia y Avila', category='Excursión', guide='Pedro Sanchez', date='2024-06-19', time='09:00', price=60.0, description='Día completo visitando ciudades patrimonio.'),
            ]
            db.session.add_all(toursData)

        # Cruises
        if Cruise.query.count() == 0:
            cruisesData = [
                Cruise(destination='Islas Griegas', ship='Aegean Star', departure_date='2024-07-01', duration=7, price=1200.0, description='Crucero de lujo por Santorini y Mykonos.'),
                Cruise(destination='Caribe', ship='Caribbean Queen', departure_date='2024-08-10', duration=10, price=1500.0, description='Sol, playa y relax en el Caribe.'),
                Cruise(destination='Fiordos Noruegos', ship='Nordic Explorer', departure_date='2024-06-25', duration=8, price=1800.0, description='Naturaleza impresionante en el norte de Europa.'),
                Cruise(destination='Mediterráneo Occidental', ship='Med Pearl', departure_date='2024-09-05', duration=7, price=900.0, description='Barcelona, Roma, Marsella.'),
            ]
            db.session.add_all(cruisesData)

        # Buses
        if Bus.query.count() == 0:
            busesData = [
                Bus(origin='Madrid', destination='Barcelona', departure_time='08:00', arrival_time='15:00', price=40.0),
                Bus(origin='Madrid', destination='Valencia', departure_time='09:00', arrival_time='13:00', price=30.0),
                Bus(origin='Sevilla', destination='Málaga', departure_time='10:00', arrival_time='12:30', price=20.0),
                Bus(origin='Bilbao', destination='San Sebastián', departure_time='11:00', arrival_time='12:00', price=15.0),
            ]
            db.session.add_all(busesData)
            
        # Trains
        if Train.query.count() == 0:
            trainsData = [
                Train(origin='Madrid', destination='Barcelona', departure_time='07:00', arrival_time='09:30', price=80.0),
                Train(origin='Madrid', destination='Sevilla', departure_time='08:30', arrival_time='11:00', price=70.0),
                Train(origin='Valencia', destination='Madrid', departure_time='16:00', arrival_time='17:45', price=65.0),
                Train(origin='Barcelona', destination='Paris', departure_time='10:00', arrival_time='16:00', price=150.0),
            ]
            db.session.add_all(trainsData)

        print("Populating Group 2 Services (Experiences, Hotels, Houses)...")
        # Experiences
        if ExperienciaCulinaria.query.count() == 0:
            exps = [
                ExperienciaCulinaria(titulo='Paella Masterclass', descripcion='Aprende a cocinar la auténtica paella valenciana.', precio=80.0, ubicacion='Valencia', imagen='https://images.unsplash.com/photo-1515443961218-a51367888e4b?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                ExperienciaCulinaria(titulo='Cata de Vinos', descripcion='Degustación de vinos premium en la Rioja.', precio=60.0, ubicacion='Logroño', imagen='https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                ExperienciaCulinaria(titulo='Ruta de Pintxos', descripcion='Explora el casco viejo de San Sebastián probando pintxos.', precio=55.0, ubicacion='San Sebastián', imagen='https://images.unsplash.com/photo-1564860074219-c637c35d648b?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                ExperienciaCulinaria(titulo='Cena Estrellas Michelin', descripcion='Experiencia gourmet inolvidable.', precio=200.0, ubicacion='Madrid', imagen='https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
            ]
            db.session.add_all(exps)

        # Hotels
        if Hotel.query.count() == 0:
            hotels = [
                Hotel(nombre='Gran Hotel Miramar', descripcion='Lujo frente al mar.', estrellas=5, precio_noche=300.0, ubicacion='Málaga', imagen='https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                Hotel(nombre='Hotel Ritz', descripcion='Elegancia clásica en el corazón de la ciudad.', estrellas=5, precio_noche=450.0, ubicacion='Madrid', imagen='https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                Hotel(nombre='Petit Palace', descripcion='Encanto boutique.', estrellas=4, precio_noche=120.0, ubicacion='Sevilla', imagen='https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                Hotel(nombre='Ibis Center', descripcion='Comodidad a buen precio.', estrellas=3, precio_noche=80.0, ubicacion='Barcelona', imagen='https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
            ]
            db.session.add_all(hotels)

        # Houses
        if CasaAlquiler.query.count() == 0:
            houses = [
                CasaAlquiler(nombre='Villa Sol', descripcion='Villa con piscina privada.', habitaciones=4, precio_dia=250.0, ubicacion='Alicante', imagen='https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                CasaAlquiler(nombre='Apartamento Centro', descripcion='Perfecto para parejas.', habitaciones=1, precio_dia=90.0, ubicacion='Granada', imagen='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
                CasaAlquiler(nombre='Casa Rural El Roble', descripcion='Escapada a la naturaleza.', habitaciones=3, precio_dia=150.0, ubicacion='Asturias', imagen='https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=800', proveedor_id=provider1.id),
            ]
            db.session.add_all(houses)

        db.session.commit()

        # Reservations (Group 1)
        user1 = User.query.filter_by(username='user1').first()
        if user1 and Reservation.query.count() == 0:
            # We need valid service IDs. Since we just populated, we can fetch some.
            tour = Tour.query.first()
            if tour:
                res1 = Reservation(service_type='tour', service_id=tour.id, quantity=2, total_price=tour.price*2, status='CONFIRMED', created_at=datetime.utcnow())
                db.session.add(res1)
                # Link to user? Reservation model (Group 1) has NO user_id field!
                # Wait, looking at models.py again.
                # class Reservation(db.Model): ... id, service_type, service_id, quantity, total_price, status ... 
                # NO USER FIELD.
                # This means Group 1 reservations are ANONYMOUS or global? 
                # Checking app.py: @app.route('/reservations') fetch all?
                # Line 89: @login_required def reservations():
                # Line 92: reservations_data = Reservation.query.order_by(Reservation.created_at.desc()).all()
                # It fetches ALL reservations in the system, regardless of user.
                # So yes, I can just create them.
                pass

        # Reservas (Group 3) - Linked to User
        if user1 and Reserva.query.count() == 0:
            # Fetch services
            exp = ExperienciaCulinaria.query.first()
            if exp:
                r1 = Reserva(usuario_id=user1.id, tipo_servicio='experience', servicio_id=exp.id, fecha_inicio=datetime.now().date(), total=exp.precio, estado='CONFIRMED')
                db.session.add(r1)
            
            hotel = Hotel.query.first()
            if hotel:
               r2 = Reserva(usuario_id=user1.id, tipo_servicio='hotel', servicio_id=hotel.id, fecha_inicio=datetime.now().date() + timedelta(days=5), total=hotel.precio_noche*3, estado='PENDING')
               db.session.add(r2)

        db.session.commit()
        print("Database populate complete!")

if __name__ == '__main__':
    populate_db()
