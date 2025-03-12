from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from admin.models import AdminUser
from database.db_config import Session

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        session = Session()
        try:
            user = session.query(AdminUser).filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page if next_page else url_for('admin.dashboard'))
            flash('Invalid username or password', 'danger')
        finally:
            session.close()

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.login'))


@admin_bp.route('/intents')
@login_required
def intents():
    return render_template('admin/intents.html')


@admin_bp.route('/responses')
@login_required
def responses():
    return render_template('admin/responses.html')

