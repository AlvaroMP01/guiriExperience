# GuiriExperience - Travel Booking Platform

## 🌍 Project Overview
GuiriExperience is a comprehensive travel booking platform that allows users to book tours, cruises, buses, trains, hotels, and unique experiences all in one place. The platform includes role-based access control for different types of sellers and administrators.

## 📋 Group 1 Responsibilities
This repository contains the frontend templates and admin panels for:
- **Tours** 🎫
- **Cruises** 🚢
- **Buses** 🚌
- **Trains** 🚆

## 📋 Group 2 Responsibilities
This repository also integrates:
- **Culinary Experiences** 🍷
- **Hotels** 🏨
- **Rental Houses** 🏡

## 📋 Group 3 Responsibilities
This repository includes:
- **User Authentication** (Login/Register) 🔒
- **Profile Management** 👤
- **Role Management** 🛡️

## 🎯 Features Implemented

### 1. User-Facing Pages
- **Index (Home Page)** - Main landing page with all services
- **Tours Page** - Browse and search available tours
- **Cruises Page** - View cruise itineraries and book cabins
- **Buses Page** - Search bus routes and buy tickets
- **Trains Page** - Check train schedules and book tickets
- **Experiences Page** - Browse culinary experiences
- **Hotels/Houses Page** - Browse accommodations
- **Reservations Page** - View and manage all bookings

### 2. Admin Panel (Unified)
A single unified admin panel manages all services:
- **Unified Admin Panel** - Manage tours, cruises, buses, trains
- **Provider Dashboard** - Manage experiences, hotels, houses

### 3. Search Functionality
All pages include real-time search and filtering.

### 4. Booking Forms
Each service includes a booking form with necessary details.

## 👥 User Roles

### Customer Roles
- **USER** - Can browse and book services

### Seller Roles (Admin Access)
- **TOUR_SELLER** - Manages tours only
- **CRUISE_SELLER** - Manages cruises only
- **BUS_SELLER** - Manages bus routes only
- **TRAIN_SELLER** - Manages train routes only
- **PROVIDER** - Manages hotels/experiences/houses
- **ADMIN** - Full access to all admin panels

## 🎨 Design Features
- Modern gradient backgrounds
- Responsive design
- Interactive cards and micro-animations

## 🔧 Technical Requirements
- Python Flask Backend
- SQLAlchemy ORM (Unified Database)
- **SQLite Database** (`guiriexperience.db`) - Replaces Group 3's MySQL requirement for ease of testing.
- Flask-Login for Authentication
- Jinja2 Templating

## 🚀 Installation & Run
1. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-loginwerkzeug
   ```
2. Run the application:
   ```bash
   python app.py
   ```
   The database tables will be created automatically.
   
3. (Optional) Create initial users:
   ```bash
   python crear_usuarios.py
   ```

---

**Integrated by GuiriExperience Team**
