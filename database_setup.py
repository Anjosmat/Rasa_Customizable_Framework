import os
import sqlite3
from typing import Generator
from pathlib import Path


class DatabaseError(Exception):
    """Custom exception for database-related errors"""
    pass


class DatabaseConnection:
    """Database connection context manager"""

    def __init__(self, db_file: str = "chatbot.db"):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        try:
            # Convert to Path object for better path handling
            db_path = Path(self.db_file)

            # Create directory if it doesn't exist (except for memory database)
            if self.db_file != ":memory:" and not db_path.parent.exists():
                try:
                    db_path.parent.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    raise DatabaseError(f"Permission denied: Cannot create directory at {db_path.parent}")
                except Exception as e:
                    raise DatabaseError(f"Failed to create database directory: {str(e)}")

            self.conn = sqlite3.connect(str(db_path))
            self.conn.execute("PRAGMA foreign_keys = ON")
            return self.conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Error connecting to database '{self.db_file}': {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def create_connection(db_file: str = "chatbot.db") -> DatabaseConnection:
    """
    Create a database connection with context management

    Args:
        db_file: Path to the SQLite database file

    Returns:
        DatabaseConnection: Database connection context manager
    """
    return DatabaseConnection(db_file)


def init_database(db_file: str = "chatbot.db") -> None:
    """
    Initialize the database with required tables and initial data

    Args:
        db_file: Path to the SQLite database file

    Raises:
        DatabaseError: If database initialization fails
    """
    try:
        with create_connection(db_file) as conn:
            cursor = conn.cursor()

            # Create tables with proper constraints
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS intents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                );

                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    intent_id INTEGER NOT NULL,
                    response_text TEXT NOT NULL,
                    FOREIGN KEY (intent_id) REFERENCES intents(id)
                );

                CREATE TABLE IF NOT EXISTS training_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    intent_id INTEGER NOT NULL,
                    example_text TEXT NOT NULL,
                    FOREIGN KEY (intent_id) REFERENCES intents(id)
                );
            """)

            # Insert initial intents if they don't exist
            initial_intents = [
                ('greet', 'Greeting messages'),
                ('goodbye', 'Farewell messages'),
                ('bot_challenge', 'Bot identity verification')
            ]

            for intent_name, description in initial_intents:
                try:
                    cursor.execute(
                        "INSERT INTO intents (name, description) VALUES (?, ?)",
                        (intent_name, description)
                    )
                except sqlite3.IntegrityError:
                    print(f"Intent '{intent_name}' already exists, skipping...")
                except sqlite3.Error as e:
                    raise DatabaseError(f"Error inserting intent '{intent_name}': {str(e)}")

            conn.commit()

    except DatabaseError:
        raise
    except Exception as e:
        raise DatabaseError(f"Unexpected error during database initialization: {str(e)}")


def verify_database_setup(db_file: str = "chatbot.db") -> bool:
    """
    Verify that the database is properly set up with all required tables

    Args:
        db_file: Path to the SQLite database file

    Returns:
        bool: True if verification passes, False otherwise

    Raises:
        DatabaseError: If verification cannot be completed
    """
    required_tables = {'intents', 'responses', 'training_data'}

    try:
        with create_connection(db_file) as conn:
            cursor = conn.cursor()

            # Get all tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = {row[0] for row in cursor.fetchall()}

            # Verify all required tables exist
            missing_tables = required_tables - existing_tables
            if missing_tables:
                raise DatabaseError(f"Missing required tables: {', '.join(missing_tables)}")

            # Verify basic data presence
            cursor.execute("SELECT COUNT(*) FROM intents")
            if cursor.fetchone()[0] == 0:
                raise DatabaseError("Database is empty: no intents found")

            return True

    except DatabaseError:
        raise
    except Exception as e:
        raise DatabaseError(f"Error during database verification: {str(e)}")


if __name__ == "__main__":
    try:
        init_database()
        if verify_database_setup():
            print("Database setup completed successfully")
    except DatabaseError as e:
        print(f"Database setup failed: {str(e)}")
