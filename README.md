# Sistema de Gestión - Proyecto

## 📋 Descripción
Sistema de gestión web con autenticación de usuarios y diferentes roles (Admin, Vendedor, Usuario).

## 🚀 Características

### ✅ Autenticación
- Sistema de login seguro con contraseñas hasheadas
- Registro de usuarios
- Gestión de sesiones con Flask-Login
- Cierre de sesión

### 👥 Roles de Usuario
- **Admin**: Administrador del sistema
- **Vendedor**: Usuario con permisos de vendedor
- **Usuario**: Usuario regular

### 📱 Páginas Disponibles
1. **Login** (`/login`) - Página de inicio de sesión
2. **Register** (`/register`) - Registro de nuevos usuarios
3. **Dashboard** (`/dashboard`) - Página principal después del login
4. **Perfil** (`/perfil`) - Visualización del perfil del usuario
5. **Editar Perfil** (`/perfil/editar`) - Edición de contraseña

## 🗄️ Base de Datos

### Tabla: `user`
- `id`: ID único del usuario
- `username`: Nombre de usuario (único)
- `password`: Contraseña hasheada
- `role`: Rol del usuario (admin, vendedor, usuario)

## 👤 Usuarios Creados

| Usuario  | Contraseña    | Rol      |
|----------|---------------|----------|
| admin    | admin123      | admin    |
| vendedor | vendedor123   | vendedor |
| usuario  | usuario123    | usuario  |

## 🛠️ Instalación y Uso

### Requisitos Previos
- Python 3.x
- XAMPP con MySQL activo
- Base de datos `loqsea` creada en MySQL

### Instalación de Dependencias
```bash
pip install flask flask-sqlalchemy flask-login pymysql werkzeug
```

### Crear Usuarios en la Base de Datos
```bash
python crear_usuarios.py
```

### Iniciar el Servidor
```bash
python app.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

## 📁 Estructura del Proyecto

```
proyectoComun/
│
├── app.py                      # Aplicación principal Flask
├── models.py                   # Modelos de base de datos
├── crear_usuarios.py           # Script para crear usuarios
│
├── Templates/
│   ├── base.html              # Template base con navbar
│   ├── login.html             # Página de login
│   ├── register.html          # Página de registro
│   ├── home.html              # Dashboard principal
│   ├── perfil.html            # Página de perfil
│   └── editar_perfil.html     # Edición de perfil
│
└── README.md                   # Este archivo
```

## 🎨 Diseño
- Diseño moderno con gradientes
- Interfaz responsive
- Colores principales: #667eea y #764ba2
- Navegación intuitiva con navbar sticky

## 🔒 Seguridad
- Contraseñas hasheadas con Werkzeug
- Protección de rutas con `@login_required`
- Validación de sesiones
- Gestión segura de cookies de sesión

## 📝 Notas
- La base de datos debe llamarse `loqsea`
- El servidor MySQL debe estar corriendo en el puerto 3306
- Usuario de MySQL: `root` (sin contraseña por defecto)

## 🔄 Próximas Mejoras
- [ ] Recuperación de contraseña
- [ ] Validación de email
- [ ] Gestión de usuarios (CRUD) para admin
- [ ] Dashboard personalizado por rol
- [ ] Estadísticas y reportes
