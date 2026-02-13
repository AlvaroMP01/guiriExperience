from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, User

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    # Página principal - accesible sin login
    return render_template('home.html', user=current_user if current_user.is_authenticated else None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            session['role'] = user.role
            
            # Redirigir al dashboard después del login exitoso
            return redirect(url_for('dashboard'))
        else:
            # Si las credenciales son incorrectas, mostrar mensaje de error
            return render_template('login.html', error='Usuario o contraseña incorrectos')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'usuario')  # Por defecto 'usuario'
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='El usuario ya existe')
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    is_admin_users = current_user.role == 'ADMIN1'
    is_admin_experiencias = current_user.role == 'ADMIN2'
    is_admin_tours = current_user.role == 'ADMIN3'
    

    if is_admin_users:
        # Mostrar dashboard con opciones de administración
        return redirect(url_for('admin_dashboard_users'))
    
    elif is_admin_experiencias:
        # Mostrar dashboard con opciones de administración de experiencias
        return redirect(url_for('admin_dashboard_experiencias'))
        

    elif is_admin_tours:
        # Mostrar dashboard con opciones de administración de tours
        return redirect(url_for('admin_dashboard_tours'))

# --- Admin Users Routes ---

@app.route('/admin/users')
@login_required
def admin_dashboard_users():
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado. Se requieren permisos de administrador de usuarios.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'error')
            return render_template('admin_user_form.html', title='Crear Usuario')
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('admin_dashboard_users'))
        
    return render_template('admin_user_form.html', title='Crear Usuario')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        
        # Update password only if provided
        if password:
            user.password = generate_password_hash(password)
            
        user.role = role
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('admin_dashboard_users'))
        
    return render_template('admin_user_form.html', title='Editar Usuario', user=user)

@app.route('/admin/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'ADMIN1':
        flash('Acceso denegado.', 'error')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario.', 'error')
        return redirect(url_for('admin_dashboard_users'))
        
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard_users'))
    

@app.route('/perfil')
@login_required
def perfil():
    # Página de perfil del usuario
    return render_template('perfil.html', user=current_user)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        # Obtener datos del formulario
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password:
            if new_password == confirm_password:
                # Actualizar contraseña
                current_user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Contraseña actualizada exitosamente', 'success')
                return redirect(url_for('perfil'))
            else:
                flash('Las contraseñas no coinciden', 'error')
        
    return render_template('editar_perfil.html', user=current_user)

if __name__ == '__main__':
    # Create tables before running the app
    with app.app_context():
        db.create_all()
        print("✓ Database tables created/verified")
    app.run(debug=True)