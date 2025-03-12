from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os
from database.models import Base  # ✅ Corrected import now pointing to correct models.

DATABASE_URL = "sqlite:///./yourdatabase.db"


class DatabaseError(Exception):
    pass


class DatabaseConnection:
    def __init__(self, db_file=DATABASE_URL):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        try:
            db_exist = os.path.exists(self.db_file.split("///")[-1])
            self.conn = create_engine(self.db_file, connect_args={"check_same_thread": False})

            # Initialize DB schema explicitly if it doesn't exist already
            if not db_exist:
                Base.metadata.create_all(self.conn)
            return self

        except OperationalError as e:
            raise DatabaseError(f"Database connection failed: {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.dispose()


def create_connection():
    return DatabaseConnection()


def init_database():
    with create_connection() as connection:
        Base.metadata.create_all(connection.conn)


def verify_database_setup():
    with create_connection() as connection:
        if not connection.conn:
            raise DatabaseError("Database setup verification failed.")
        else:
            print("Database connected successfully.")
