"""
Script to create an admin user in the database.
"""
from werkzeug.security import generate_password_hash
from database.db_config import SessionLocal, engine, Base
from admin.models import AdminUser


def create_admin_user(name, email, password):
    """Create an admin user in the database."""
    # Create a database session
    session = SessionLocal()

    try:
        # Check if user with this email already exists
        existing_user = session.query(AdminUser).filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return

        # Create a new admin user
        hashed_password = generate_password_hash(password)
        admin = AdminUser(
            name=name,
            email=email,
            password=hashed_password,
            is_admin=True
        )

        # Add to database and commit
        session.add(admin)
        session.commit()
        print(f"Admin user '{name}' with email '{email}' created successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error creating admin user: {str(e)}")

    finally:
        session.close()


if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Create admin user
    create_admin_user(
        name="Admin User",
        email="admin@example.com",
        password="admin123"
    )