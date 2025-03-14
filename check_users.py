from database.db_config import SessionLocal
from admin.models import AdminUser


def check_users():
    session = SessionLocal()
    users = session.query(AdminUser).all()

    print(f"Found {len(users)} users in the database:")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Is Admin: {user.is_admin}")

    session.close()


if __name__ == "__main__":
    check_users()