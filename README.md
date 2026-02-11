<<<<<<< HEAD
# GuiriExperience - Travel Booking Platform

## 🌍 Project Overview
GuiriExperience is a comprehensive travel booking platform that allows users to book tours, cruises, buses, and trains all in one place. The platform includes role-based access control for different types of sellers and administrators.

## 📋 Group 1 Responsibilities
This repository contains the frontend templates and admin panels for:
- **Tours** 🎫
- **Cruises** 🚢
- **Buses** 🚌
- **Trains** 🚆

## 🎯 Features Implemented

### 1. User-Facing Pages
- **Index (Home Page)** - Main landing page with service cards
- **Tours Page** - Browse and search available tours
- **Cruises Page** - View cruise itineraries and book cabins
- **Buses Page** - Search bus routes and buy tickets
- **Trains Page** - Check train schedules and book tickets
- **Reservations Page** - View and manage all bookings

### 2. Admin Panel (Role-Based Access)
A single unified admin panel manages all services:
- **Unified Admin Panel** - Manage tours, cruises, buses, and trains in one interface with tabs

### 3. Search Functionality
All pages include real-time search and filtering:
- **Tours**: Search by name, category, guide, and date
- **Cruises**: Search by destination, ship, date, and duration
- **Buses**: Search by origin, destination, and time
- **Trains**: Search by origin, destination, and time

### 4. Booking Forms
Each service includes a booking form with:
- Service selection
- Passenger/ticket quantity
- Additional options (cabin type, seat preference, class)

## 👥 User Roles

### Customer Roles
- **USER** - Can browse and book services

### Seller Roles (Admin Access)
- **TOUR_SELLER** - Manages tours only
- **CRUISE_SELLER** - Manages cruises only
- **BUS_SELLER** - Manages bus routes only
- **TRAIN_SELLER** - Manages train routes only
- **ADMIN** - Full access to all admin panels

## 🎨 Design Features
- Modern gradient backgrounds for each service
- Responsive design
- Real-time search filtering
- Interactive cards and buttons
- Clean, professional UI

## 📁 File Structure
```
templates/
├── index.html              # Home page
├── tours.html              # Tours booking page
├── cruceros.html           # Cruises booking page
├── bus.html                # Bus booking page
├── trenes.html             # Trains booking page
├── reservas.html           # Reservations management
└── admin.html              # Unified admin panel for all services
```

## 🔧 Technical Requirements

### Backend Integration (To be implemented by other groups)
The templates expect the following Flask routes:

#### Main Routes
- `GET /` - index()
- `GET /tours` - tours()
- `GET /cruises` - cruises()
- `GET /buses` - buses()
- `GET /trains` - trains()
- `GET /reservations` - reservations()

#### Admin Routes
- `GET /admin` - admin() - Unified admin panel for all services

#### Booking Routes
- `POST /tours/<id>/book` - book_tour()
- `POST /cruises/book` - book_cruise()
- `POST /buses/book` - book_bus_ticket()
- `POST /trains/book` - book_train_ticket()

#### CRUD Operations
- `POST /admin/tours/add` - add_tour()
- `POST /admin/cruises/add` - add_cruise()
- `POST /admin/buses/add` - add_bus_route()
- `POST /admin/trains/add` - add_train_route()
- `POST /admin/<service>/<id>/edit` - edit operations
- `POST /admin/<service>/<id>/delete` - delete operations

### Database Schema (To be implemented by other groups)

#### Required Tables
- `users` - User accounts
- `tours` - Tour listings
- `cruises` - Cruise itineraries
- `buses` - Bus routes
- `trains` - Train routes
- `reservations` - All bookings
- `tour_guides` - Tour guide information
- `captains` - Cruise captains
- `ships` - Cruise ships
- `ports` - Cruise ports
- `drivers` - Bus drivers
- `conductors` - Train conductors
- `stations` - Train stations

### Session Variables Expected
- `session['user_id']` - Current user ID
- `session['role']` - User role (ADMIN, TOUR_SELLER, etc.)

## 🌐 Standardization
- ✅ All code in **ENGLISH**
- ✅ All roles in **UPPERCASE**
- ✅ Consistent naming conventions
- ✅ Modern, professional design

## 🚀 Next Steps (For Integration)
1. Backend team implements Flask routes
2. Database team creates MySQL schema
3. Connect forms to backend endpoints
4. Implement authentication system
5. Add data validation
6. Test all booking flows

## 📝 Notes
- All templates use Jinja2 templating
- JavaScript included for real-time search
- Forms use POST method for security
- Admin panels check user roles via session

## 👨‍💼 Team Coordination
- **Group 1 (This group)**: Tours, Cruises, Buses, Trains (Frontend + Admin Panels)
- **Group 2**: User authentication and accessibility
- **Group 3**: Other features

---

**Created by Group 1 - GuiriExperience Team**
=======
# guiriExperience
>>>>>>> 86977553ed569ab90cfc4f9b48d0af0fb0319882
