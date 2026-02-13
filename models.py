<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==================== GRUPO1 MODELS (Tours, Cruises, Buses, Trains) ====================

class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    guide = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    seats_available = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'date': self.date,
            'time': self.time
        }

class Cruise(db.Model):
    __tablename__ = 'cruises'
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    ship = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    seats_available = db.Column(db.Integer, default=200)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(5), nullable=False)
    arrival_time = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Train(db.Model):
    __tablename__ = 'trains'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(5), nullable=False)
    arrival_time = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    service_type = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='CONFIRMED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_service_details(self):
        """Helper to get details depending on service_type"""
        return f"{self.service_type.capitalize()} #{self.service_id}"

# ==================== GRUPO2 MODELS (Users, Experiences, Hotels, Houses) ====================

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

class ExperienciaCulinaria(db.Model):
    __tablename__ = 'experiencias_culinarias'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

class Hotel(db.Model):
    __tablename__ = 'hoteles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estrellas = db.Column(db.Integer, default=3)
    precio_noche = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

class CasaAlquiler(db.Model):
    __tablename__ = 'casas_alquiler'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    habitaciones = db.Column(db.Integer, nullable=False)
    precio_dia = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_servicio = db.Column(db.String(50), nullable=False)
    servicio_id = db.Column(db.Integer, nullable=False)
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='PENDING')
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/guiriexperience'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def get_username(self):
        return self.username
    
    def get_role(self):
        return self.role

>>>>>>> origin/grupo-3
