# 🚀 GuiriExperience - Cómo Ejecutar el Backend

## 📋 Requisitos Previos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

## ⚙️ Instalación

### 1. Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask (framework web)
- Werkzeug (utilidades para Flask)

### 2. Iniciar el Servidor

Ejecuta el siguiente comando:

```bash
python app.py
```

El servidor se iniciará en: **http://localhost:5000**

## 🔐 Credenciales de Prueba

### Usuario Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Rol:** ADMIN (acceso completo al panel de administración)

## 📱 Páginas Disponibles

### Páginas Públicas:
- **Home:** http://localhost:5000/
- **Tours:** http://localhost:5000/tours
- **Cruceros:** http://localhost:5000/cruises
- **Buses:** http://localhost:5000/buses
- **Trenes:** http://localhost:5000/trains

### Autenticación:
- **Login:** http://localhost:5000/login
- **Registro:** http://localhost:5000/register

### Panel de Administración (requiere login):
- **Admin Panel:** http://localhost:5000/admin

## 🎯 Funcionalidades del Backend

### ✅ Autenticación
- ✅ Registro de usuarios
- ✅ Login/Logout
- ✅ Sesiones seguras
- ✅ Roles de usuario (ADMIN, SELLER, USER)

### ✅ Panel de Administración
- ✅ **Tours:** Crear, editar, eliminar
- ✅ **Cruceros:** Crear, editar, eliminar
- ✅ **Buses:** Crear, editar, eliminar
- ✅ **Trenes:** Crear, editar, eliminar
- ✅ **Estadísticas:** Total de servicios, reservas, ingresos

### ✅ Base de Datos
- ✅ SQLite (archivo: `guiriexperience.db`)
- ✅ Tablas: users, tours, cruises, buses, trains, reservations
- ✅ Datos de ejemplo precargados

## 🗄️ Estructura de la Base de Datos

### Tabla: users
- id, username, email, password (hash), role, created_at

### Tabla: tours
- id, name, category, guide, date, time, price, description, created_at

### Tabla: cruises
- id, destination, ship, departure_date, duration, price, description, created_at

### Tabla: buses
- id, origin, destination, departure_time, arrival_time, price, seats_available, created_at

### Tabla: trains
- id, origin, destination, departure_time, arrival_time, price, seats_available, created_at

### Tabla: reservations
- id, user_id, service_type, service_id, quantity, total_price, status, created_at

## 🔧 Rutas de la API

### Autenticación:
- `GET/POST /login` - Iniciar sesión
- `GET/POST /register` - Registrar nuevo usuario
- `GET /logout` - Cerrar sesión

### Admin - Tours:
- `POST /admin/tour/add` - Añadir tour
- `GET/POST /admin/tour/<id>/edit` - Editar tour
- `POST /admin/tour/<id>/delete` - Eliminar tour

### Admin - Cruises:
- `POST /admin/cruise/add` - Añadir crucero
- `POST /admin/cruise/<id>/delete` - Eliminar crucero

### Admin - Buses:
- `POST /admin/bus/add` - Añadir ruta de bus
- `POST /admin/bus/<id>/delete` - Eliminar ruta

### Admin - Trains:
- `POST /admin/train/add` - Añadir ruta de tren
- `POST /admin/train/<id>/delete` - Eliminar ruta

## 🎨 Características

1. **Datos de Ejemplo:** La base de datos se crea automáticamente con datos de ejemplo
2. **Seguridad:** Contraseñas hasheadas con Werkzeug
3. **Sesiones:** Manejo seguro de sesiones de usuario
4. **Decoradores:** `@login_required` y `@admin_required` para proteger rutas
5. **Flash Messages:** Mensajes de éxito/error para feedback al usuario

## 📝 Notas Importantes

- La base de datos se crea automáticamente al iniciar la aplicación por primera vez
- El archivo `guiriexperience.db` contiene todos los datos
- Para resetear la base de datos, simplemente elimina el archivo `guiriexperience.db` y reinicia la aplicación
- El modo `debug=True` está activado para desarrollo (desactivar en producción)

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia 5000 a 5001
```

### La base de datos no se crea
Verifica que tienes permisos de escritura en la carpeta del proyecto.

## 🎉 ¡Listo!

Ahora puedes:
1. Iniciar sesión con `admin` / `admin123`
2. Acceder al panel de administración
3. Añadir, editar y eliminar servicios
4. Ver las estadísticas en tiempo real

**¡Disfruta de GuiriExperience!** 🌍✈️
