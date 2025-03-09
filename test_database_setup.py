import os
from database_setup import init_database, verify_database_setup, create_connection, DatabaseError


def run_tests():
    print("=== Running Database Setup Tests ===")

    # Test 1: Basic initialization
    print("\n1. Testing basic database initialization...")
    try:
        init_database()
        print("Database setup completed successfully.")
    except DatabaseError as e:
        print(f"Database initialization failed: {str(e)}")

    # Test 2: Testing duplicate handling
    print("\n2. Testing duplicate data handling...")
    try:
        init_database()  # Should show "already exists" messages
        print("Database setup completed successfully.")
    except DatabaseError as e:
        print(f"Database initialization failed: {str(e)}")

    # Test 3: Database verification
    print("\n3. Testing database verification...")
    try:
        result = verify_database_setup()
        print(f"Verification result: {result}")
    except DatabaseError as e:
        print(f"Database verification failed: {str(e)}")

    # Test 4: Invalid path test
    print("\n4. Testing invalid database path...")
    try:
        test_path = os.path.join("nonexistent_folder", "test.db")
        init_database(test_path)
    except DatabaseError as e:
        print(f"Database initialization failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    # Test 5: Query test
    print("\n5. Testing database queries...")
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM intents")
            results = cursor.fetchall()
            print(f"Found {len(results)} intents in database")
            for row in results:
                print(f"Intent: {row}")
    except DatabaseError as e:
        print(f"Database query failed: {str(e)}")
    except Exception as e:
        print(f"Unexpected error during query: {str(e)}")


if __name__ == "__main__":
    print("Starting database tests...")

    # Clean up existing database file before tests
    try:
        if os.path.exists("chatbot.db"):
            os.remove("chatbot.db")
            print("Removed existing database file.")
    except PermissionError:
        print("Warning: Could not remove existing database file - permission denied.")
    except Exception as e:
        print(f"Warning: Could not remove existing database file - {str(e)}")

    run_tests()
