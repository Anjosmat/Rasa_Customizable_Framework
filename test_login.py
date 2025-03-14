from werkzeug.security import check_password_hash
from database.db_config import SessionLocal
from admin.models import AdminUser


def test_login(email, password):
    session = SessionLocal()
    user = session.query(AdminUser).filter_by(email=email).first()

    if not user:
        print(f"No user found with email: {email}")
        return

    print(f"Found user: {user.name}, password hash: {user.password[:20]}...")

    if check_password_hash(user.password, password):
        print("Password is correct! Login would succeed.")
    else:
        print("Password is incorrect. Login would fail.")

    session.close()


if __name__ == "__main__":
    test_login("admin@example.com", "admin123")