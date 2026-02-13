from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# User model is handled by another team
# form .user import User

@dataclass
class Tour:
    id: int
    name: str
    category: str
    guide: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    price: float
    description: Optional[str] = None
    seats_available: int = 30
    created_at: Optional[datetime] = None

@dataclass
class Cruise:
    id: int
    destination: str
    ship: str
    departure_date: str  # YYYY-MM-DD
    duration: int
    price: float
    description: Optional[str] = None
    seats_available: int = 200
    created_at: Optional[datetime] = None

@dataclass
class Bus:
    id: int
    origin: str
    destination: str
    departure_time: str  # HH:MM
    arrival_time: str    # HH:MM
    price: float
    seats_available: int = 50
    created_at: Optional[datetime] = None

@dataclass
class Train:
    id: int
    origin: str
    destination: str
    departure_time: str  # HH:MM
    arrival_time: str    # HH:MM
    price: float
    seats_available: int = 100
    created_at: Optional[datetime] = None

@dataclass
class Reservation:
    id: int
    user_id: int
    service_type: str  # 'tour', 'cruise', 'bus', 'train'
    service_id: int
    quantity: int
    total_price: float
    status: str = 'CONFIRMED'
    created_at: Optional[datetime] = None
    
    # Helper property for frontend display logic
    @property
    def service_details(self) -> str:
        """Helper to return a summary string of the service booked"""
        # In a real app with ORM, this would access the related object
        return f"{self.service_type.capitalize()} #{self.service_id}"
