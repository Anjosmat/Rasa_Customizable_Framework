from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from database.db_config import init_db, Session
from admin.models import AdminUser

# Initialize Flask-Login
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    session = Session()
    try:
        return session.query(AdminUser).get(int(user_id))
    finally:
        session.close()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure key

    # Initialize database
    init_db()

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    # Initialize Flask-Admin
    admin = Admin(app, name='Rasa Admin', template_mode='bootstrap4')

    # Register blueprints
    from admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
