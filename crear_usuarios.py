"""
Script para crear 3 usuarios en la base de datos:
1. Admin (rol: admin)
2. Vendedor (rol: vendedor)
3. Usuario (rol: usuario)
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def crear_usuarios():
    """Crea los 3 usuarios solicitados"""
    with app.app_context():
        # Primero crear las tablas si no existen
        db.create_all()
        print("Tablas verificadas/creadas\n")
        
        # Definir los usuarios a crear
        usuarios = [
            ('admin', 'admin123', 'admin', 'Administrador del sistema'),
            ('vendedor', 'vendedor123', 'vendedor', 'Vendedor'),
            ('usuario', 'usuario123', 'usuario', 'Usuario regular')
        ]
        
        print("Creando usuarios en la base de datos...\n")
        print("="*70)
        
        usuarios_creados = 0
        
        for username, password, role, descripcion in usuarios:
            # Verificar si el usuario ya existe
            usuario_existente = User.query.filter_by(username=username).first()
            
            if usuario_existente:
                print(f"Usuario '{username}' ya existe - OMITIDO")
            else:
                # Crear nuevo usuario
                email = f"{username}@example.com"
                nuevo_usuario = User(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    role=role
                )
                db.session.add(nuevo_usuario)
                usuarios_creados += 1
                print(f"Usuario '{username}' creado exitosamente ({descripcion})")
        
        # Guardar cambios en la base de datos
        if usuarios_creados > 0:
            db.session.commit()
            print("\n" + "="*70)
            print(f"{usuarios_creados} usuario(s) creado(s) y guardado(s) en la base de datos")
        else:
            print("\n" + "="*70)
            print("Todos los usuarios ya existían en la base de datos")
        
        # Mostrar credenciales
        print("\n" + "="*70)
        print("CREDENCIALES DE ACCESO:")
        print("="*70)
        print(f"{'ROL':<15} | {'USUARIO':<15} | {'CONTRASEÑA':<15}")
        print("-"*70)
        for username, password, role, _ in usuarios:
            print(f"{role:<15} | {username:<15} | {password:<15}")
        print("="*70)
        
        # Verificar usuarios en la base de datos
        print("\nUsuarios en la base de datos:")
        print("-"*70)
        todos_usuarios = User.query.all()
        for user in todos_usuarios:
            print(f"  ID: {user.id} | Usuario: {user.username:<15} | Rol: {user.role}")
        print("="*70)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SCRIPT DE CREACIÓN DE USUARIOS")
    print("="*70 + "\n")
    crear_usuarios()
    print("\nProceso completado. Puedes iniciar la aplicación con: python app.py")
    print()
