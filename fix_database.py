"""
Script to fix database schema issues by adding missing columns
"""
import sqlite3
import os


def check_and_fix_database():
    # Path to the database file
    db_path = "database/business_data.db"

    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database file {db_path} not found!")
        return

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get current columns in business_intents table
    cursor.execute("PRAGMA table_info(business_intents)")
    columns = [column[1] for column in cursor.fetchall()]

    # Check if training_examples column exists
    if "training_examples" not in columns:
        print("Adding 'training_examples' column to business_intents table...")
        try:
            cursor.execute("ALTER TABLE business_intents ADD COLUMN training_examples TEXT DEFAULT ''")
            conn.commit()
            print("Column added successfully!")
        except sqlite3.Error as e:
            print(f"Error adding column: {e}")
            conn.rollback()
    else:
        print("Column 'training_examples' already exists.")

    # Close the connection
    conn.close()
    print("Database check complete.")


if __name__ == "__main__":
    check_and_fix_database()