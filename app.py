from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

from database.db_config import SessionLocal, engine, Base
from admin.models import AdminUser
from admin.routes import admin_bp

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/business_data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable debug mode
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(AdminUser).get(int(user_id))
    db.close()
    return user


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        app.logger.debug(f"Login attempt for email: {email}")

        db = SessionLocal()
        user = db.query(AdminUser).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            app.logger.debug(f"Login successful for user: {user.name}")
            login_user(user)
            db.close()
            return redirect(url_for('admin.dashboard'))

        app.logger.debug(f"Login failed for email: {email}")
        db.close()
        flash('Invalid email or password')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# API Routes for chatbot
@app.route('/api/chat', methods=['POST'])
def chat_api():
    """
    API endpoint for the chatbot frontend to communicate with Rasa
    """
    data = request.json
    # Process data and forward to Rasa
    # This is a placeholder for the actual Rasa integration
    return jsonify({"message": "Hello from the chatbot!"})


if __name__ == '__main__':
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Check if admin user exists, if not create one
    db = SessionLocal()
    admin = db.query(AdminUser).filter_by(email='admin@example.com').first()
    if not admin:
        hashed_password = generate_password_hash('admin123')
        admin = AdminUser(
            name='Admin',
            email='admin@example.com',
            password=hashed_password,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("Admin user created!")
    db.close()

    app.run(debug=True, port=5000)