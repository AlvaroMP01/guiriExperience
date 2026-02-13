from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy (in a real app, this might be imported from extensions.py or app.py)
db = SQLAlchemy()

# Models based on the schema defined in app.py

class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    guide = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False) # Storing as string YYYY-MM-DD for consistency with current app
    time = db.Column(db.String(5), nullable=False)  # Storing as string HH:MM
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
    duration = db.Column(db.Integer, nullable=False) # In days
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
    user_id = db.Column(db.Integer, nullable=False) # Linked to User model from the other group
    service_type = db.Column(db.String(20), nullable=False) # 'tour', 'cruise', 'bus', 'train'
    service_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='CONFIRMED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_service_details(self):
        """Helper to get details depending on service_type"""
        return f"{self.service_type.capitalize()} #{self.service_id}"
