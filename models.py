from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False) 
    # Suggested Roles: 'CUSTOMER', 'PROVIDER', 'ADMIN'

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
    tipo_servicio = db.Column(db.String(50), nullable=False) # 'experience', 'hotel', 'house'
    servicio_id = db.Column(db.Integer, nullable=False) # ID from the corresponding table
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True) # Only for hotel/house
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='PENDING') # 'PENDING', 'CONFIRMED', 'CANCELLED'
