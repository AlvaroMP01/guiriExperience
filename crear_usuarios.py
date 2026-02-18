"""
Script para crear usuarios con los roles correctos (UPPERCASE)
Sincroniza los usuarios de prueba con la lógica de app.py
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def crear_usuarios():
    """Crea o actualiza los usuarios solicitados con roles correctos"""
    with app.app_context():
        # Primero crear las tablas si no existen
        db.create_all()
        print("Tablas verificadas/creadas\n")
        
        # Definir los usuarios a crear/actualizar
        # Formato: (username, password, role, descripcion)
        usuarios = [
            ('admin', 'admin123', 'ADMIN', 'Administrador Global (Todos los paneles)'),
            ('vendedor', 'vendedor123', 'TOUR_SELLER', 'Vendedor Transporte (Panel Transporte)'),
            ('provider', 'provider123', 'PROVIDER', 'Proveedor Alojamiento (Panel Experiencias)'),
            ('usuario', 'usuario123', 'USER', 'Usuario Final (Solo Reservas)')
        ]
        
        print("Actualizando usuarios en la base de datos...\n")
        print("="*70)
        
        usuarios_procesados = 0
        
        for username, password, role, descripcion in usuarios:
            # Buscar usuario existente
            usuario = User.query.filter_by(username=username).first()
            
            if usuario:
                print(f"Usuario '{username}' encontrado. Actualizando rol/password...")
                usuario.role = role
                # Opcional: actualizar password siempre para asegurar acceso
                usuario.password = generate_password_hash(password)
                usuario.email = f"{username}@example.com"
                print(f" -> Rol actualizado a: {role}")
            else:
                print(f"Usuario '{username}' NO existe. Creando...")
                nuevo_usuario = User(
                    username=username,
                    email=f"{username}@example.com",
                    password=generate_password_hash(password),
                    role=role
                )
                db.session.add(nuevo_usuario)
            
            usuarios_procesados += 1
            
        # Guardar cambios
        try:
            db.session.commit()
            print("\n" + "="*70)
            print(f"{usuarios_procesados} usuarios procesados correctamente.")
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: {e}")
        
        # Mostrar credenciales finales
        print("\n" + "="*70)
        print("CREDENCIALES DE ACCESO ACTUALIZADAS:")
        print("="*70)
        print(f"{'ROL (SISTEMA)':<15} | {'USUARIO':<15} | {'CONTRASEÑA':<15} | {'ACCESO'}")
        print("-"*90)
        for username, password, role, desc in usuarios:
            acceso = "Todo" if role == 'ADMIN' else ("Transp." if 'SELLER' in role else ("Alojam." if 'PROVIDER' in role else "Web"))
            print(f"{role:<15} | {username:<15} | {password:<15} | {acceso}")
        print("="*70)

if __name__ == '__main__':
    crear_usuarios()
