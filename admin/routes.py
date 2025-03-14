from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from database.db_config import SessionLocal, Business, BusinessIntent, BotConfig
from admin.models import AdminUser, ChatbotLog

admin_bp = Blueprint('admin', __name__)


# Helper function to check admin privileges
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin privileges required')
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


# Admin Dashboard
@admin_bp.route('/')
@login_required
def dashboard():
    db = SessionLocal()

    # Get counts for dashboard stats
    business_count = db.query(Business).count()
    intent_count = db.query(BusinessIntent).count()
    user_count = db.query(AdminUser).count()

    # Get recent logs
    logs = db.query(ChatbotLog).order_by(ChatbotLog.id.desc()).limit(10).all()

    db.close()

    return render_template('admin/dashboard.html',
                           business_count=business_count,
                           intent_count=intent_count,
                           user_count=user_count,
                           logs=logs)


# Business Management
@admin_bp.route('/businesses')
@admin_required
def businesses():
    db = SessionLocal()
    businesses = db.query(Business).all()
    db.close()
    return render_template('admin/businesses.html', businesses=businesses)


@admin_bp.route('/businesses/new', methods=['GET', 'POST'])
@admin_required
def new_business():
    if request.method == 'POST':
        name = request.form.get('name')
        business_type = request.form.get('business_type')
        contact_email = request.form.get('contact_email')

        db = SessionLocal()
        try:
            # Create new business
            business = Business(
                name=name,
                business_type=business_type,
                contact_email=contact_email,
                is_active=True
            )
            db.add(business)

            # Create default bot config
            config = BotConfig(
                business_type=business_type,
                default_greeting=f"Welcome to {name}! How can I help you today?",
                default_fallback="I'm not sure I understand. Could you rephrase that?"
            )
            db.add(config)

            db.commit()
            flash(f"Business '{name}' created successfully!")
        except SQLAlchemyError as e:
            db.rollback()
            flash(f"Error creating business: {str(e)}")
        finally:
            db.close()

        return redirect(url_for('admin.businesses'))

    return render_template('admin/new_business.html')


@admin_bp.route('/businesses/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_business(id):
    db = SessionLocal()
    business = db.query(Business).get(id)

    if not business:
        db.close()
        flash("Business not found")
        return redirect(url_for('admin.businesses'))

    if request.method == 'POST':
        business.name = request.form.get('name')
        business.business_type = request.form.get('business_type')
        business.contact_email = request.form.get('contact_email')
        business.is_active = 'is_active' in request.form

        try:
            db.commit()
            flash("Business updated successfully!")
        except SQLAlchemyError as e:
            db.rollback()
            flash(f"Error updating business: {str(e)}")

    db.close()
    return render_template('admin/edit_business.html', business=business)


@admin_bp.route('/delete_business/<int:id>', methods=['POST'])
@admin_required
def delete_business(id):
    db = SessionLocal()
    business = db.query(Business).get(id)

    if not business:
        db.close()
        flash("Business not found")
        return redirect(url_for('admin.businesses'))

    try:
        db.delete(business)
        db.commit()
        flash(f"Business '{business.name}' deleted successfully!")
    except SQLAlchemyError as e:
        db.rollback()
        flash(f"Error deleting business: {str(e)}")

    db.close()
    return redirect(url_for('admin.businesses'))


# Intent Management
@admin_bp.route('/intents')
@login_required
def intents():
    db = SessionLocal()

    # Filter by business type if user is not admin
    if current_user.is_admin:
        intents = db.query(BusinessIntent).all()
    else:
        # For business users, only show their business intents
        business = db.query(Business).get(current_user.business_id)
        if business:
            intents = db.query(BusinessIntent).filter_by(business_type=business.business_type).all()
        else:
            intents = []

    db.close()
    return render_template('admin/intents.html', intents=intents)


@admin_bp.route('/intents/new', methods=['GET', 'POST'])
@login_required
def new_intent():
    db = SessionLocal()

    # Get available business types
    if current_user.is_admin:
        businesses = db.query(Business).all()
    else:
        # For business users, only show their business
        businesses = db.query(Business).filter_by(id=current_user.business_id).all()

    if request.method == 'POST':
        business_type = request.form.get('business_type')
        intent_name = request.form.get('intent_name')
        response_text = request.form.get('response_text')
        training_examples = request.form.get('training_examples')

        # Check if intent already exists
        existing = db.query(BusinessIntent).filter_by(
            business_type=business_type,
            intent_name=intent_name
        ).first()

        if existing:
            flash(f"Intent '{intent_name}' already exists for this business type")
        else:
            try:
                intent = BusinessIntent(
                    business_type=business_type,
                    intent_name=intent_name,
                    response_text=response_text,
                    training_examples=training_examples
                )
                db.add(intent)
                db.commit()
                flash(f"Intent '{intent_name}' created successfully!")

                # TODO: Call function to regenerate NLU file

            except SQLAlchemyError as e:
                db.rollback()
                flash(f"Error creating intent: {str(e)}")

        return redirect(url_for('admin.intents'))

    db.close()
    return render_template('admin/new_intent.html', businesses=businesses)


@admin_bp.route('/intents/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_intent(id):
    db = SessionLocal()
    intent = db.query(BusinessIntent).get(id)

    if not intent:
        db.close()
        flash("Intent not found")
        return redirect(url_for('admin.intents'))

    # Check if user has permission
    if not current_user.is_admin:
        business = db.query(Business).get(current_user.business_id)
        if not business or business.business_type != intent.business_type:
            db.close()
            flash("You don't have permission to edit this intent")
            return redirect(url_for('admin.intents'))

    if request.method == 'POST':
        intent.response_text = request.form.get('response_text')
        intent.training_examples = request.form.get('training_examples')

        try:
            db.commit()
            flash("Intent updated successfully!")

            # TODO: Call function to regenerate NLU file

        except SQLAlchemyError as e:
            db.rollback()
            flash(f"Error updating intent: {str(e)}")

    db.close()
    return render_template('admin/edit_intent.html', intent=intent)


@admin_bp.route('/delete_intent/<int:id>', methods=['POST'])
@login_required
def delete_intent(id):
    db = SessionLocal()
    intent = db.query(BusinessIntent).get(id)

    if not intent:
        db.close()
        flash("Intent not found")
        return redirect(url_for('admin.intents'))

    # Check if user has permission
    if not current_user.is_admin:
        business = db.query(Business).get(current_user.business_id)
        if not business or business.business_type != intent.business_type:
            db.close()
            flash("You don't have permission to delete this intent")
            return redirect(url_for('admin.intents'))

    try:
        db.delete(intent)
        db.commit()
        flash(f"Intent '{intent.intent_name}' deleted successfully!")
    except SQLAlchemyError as e:
        db.rollback()
        flash(f"Error deleting intent: {str(e)}")

    db.close()
    return redirect(url_for('admin.intents'))


# User Management (Admin only)
@admin_bp.route('/users')
@admin_required
def users():
    db = SessionLocal()

    try:
        # Fetch all users
        users_list = db.query(AdminUser).all()

        # Prefetch business data to avoid detached instance errors
        user_data = []
        for user in users_list:
            user_info = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin,
                'business_id': user.business_id,
                'business': None
            }

            # If user has a business_id, fetch the business
            if user.business_id:
                business = db.query(Business).get(user.business_id)
                if business:
                    user_info['business'] = {
                        'name': business.name,
                        'business_type': business.business_type
                    }

            user_data.append(user_info)

        # Get all businesses for the dropdown
        businesses = db.query(Business).all()
        business_list = [{'id': b.id, 'name': b.name, 'business_type': b.business_type} for b in businesses]

    finally:
        db.close()

    return render_template('admin/users.html', users=user_data, businesses=business_list)


@admin_bp.route('/users/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    from werkzeug.security import generate_password_hash

    db = SessionLocal()
    businesses = db.query(Business).all()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        business_id = request.form.get('business_id')

        if business_id == "":
            business_id = None
        else:
            business_id = int(business_id)

        # Check if user already exists
        existing = db.query(AdminUser).filter_by(email=email).first()

        if existing:
            flash(f"User with email '{email}' already exists")
        else:
            try:
                hashed_password = generate_password_hash(password)
                user = AdminUser(
                    name=name,
                    email=email,
                    password=hashed_password,
                    is_admin=is_admin,
                    business_id=business_id
                )
                db.add(user)
                db.commit()
                flash(f"User '{name}' created successfully!")
            except SQLAlchemyError as e:
                db.rollback()
                flash(f"Error creating user: {str(e)}")

        return redirect(url_for('admin.users'))

    db.close()
    return render_template('admin/new_user.html', businesses=businesses)


@admin_bp.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    db = SessionLocal()
    user = db.query(AdminUser).get(id)
    businesses = db.query(Business).all()

    if not user:
        db.close()
        flash("User not found")
        return redirect(url_for('admin.users'))

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')

        if request.form.get('password'):
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(request.form.get('password'))

        user.is_admin = 'is_admin' in request.form

        business_id = request.form.get('business_id')
        if business_id == "":
            user.business_id = None
        else:
            user.business_id = int(business_id)

        try:
            db.commit()
            flash("User updated successfully!")
        except SQLAlchemyError as e:
            db.rollback()
            flash(f"Error updating user: {str(e)}")

    db.close()
    return render_template('admin/edit_user.html', user=user, businesses=businesses)


@admin_bp.route('/delete_user/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    db = SessionLocal()
    user = db.query(AdminUser).get(id)

    if not user:
        db.close()
        flash("User not found")
        return redirect(url_for('admin.users'))

    try:
        db.delete(user)
        db.commit()
        flash(f"User '{user.name}' deleted successfully!")
    except SQLAlchemyError as e:
        db.rollback()
        flash(f"Error deleting user: {str(e)}")

    db.close()
    return redirect(url_for('admin.users'))


# Bot Configuration
@admin_bp.route('/bot-config')
@login_required
def bot_config():
    db = SessionLocal()

    # Filter by business type if user is not admin
    if current_user.is_admin:
        configs = db.query(BotConfig).all()
    else:
        # For business users, only show their business config
        business = db.query(Business).get(current_user.business_id)
        if business:
            configs = db.query(BotConfig).filter_by(business_type=business.business_type).all()
        else:
            configs = []

    db.close()
    return render_template('admin/bot_config.html', configs=configs)


@admin_bp.route('/bot-config/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_bot_config(id):
    db = SessionLocal()
    config = db.query(BotConfig).get(id)

    if not config:
        db.close()
        flash("Configuration not found")
        return redirect(url_for('admin.bot_config'))

    # Check if user has permission
    if not current_user.is_admin:
        business = db.query(Business).get(current_user.business_id)
        if not business or business.business_type != config.business_type:
            db.close()
            flash("You don't have permission to edit this configuration")
            return redirect(url_for('admin.bot_config'))

    if request.method == 'POST':
        config.default_greeting = request.form.get('default_greeting')
        config.default_fallback = request.form.get('default_fallback')
        config.enable_voice_support = 'enable_voice_support' in request.form
        config.enable_multilingual = 'enable_multilingual' in request.form

        try:
            db.commit()
            flash("Configuration updated successfully!")
        except SQLAlchemyError as e:
            db.rollback()
            flash(f"Error updating configuration: {str(e)}")

    db.close()
    return render_template('admin/edit_bot_config.html', config=config)


# Logs
@admin_bp.route('/logs')
@login_required
def logs():
    db = SessionLocal()

    # Filter by business if user is not admin
    if current_user.is_admin:
        logs = db.query(ChatbotLog).order_by(ChatbotLog.id.desc()).limit(100).all()
    else:
        logs = db.query(ChatbotLog).filter_by(
            business_id=current_user.business_id
        ).order_by(ChatbotLog.id.desc()).limit(100).all()

    db.close()
    return render_template('admin/logs.html', logs=logs)