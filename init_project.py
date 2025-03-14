"""
Rasa Customizable Framework Initialization Script

This script sets up the directory structure and initializes the database
for the Rasa Customizable Framework project.
"""

import os
import sys
import shutil
import sqlite3
import subprocess
from werkzeug.security import generate_password_hash


def create_directory_structure():
    """Create the necessary directory structure if it doesn't exist."""
    directories = [
        "admin",
        "admin/templates",
        "admin/templates/admin",
        "database",
        "static",
        "static/css",
        "static/js",
        "templates",
        "templates/admin",
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


def initialize_database():
    """Initialize the SQLite database with required tables."""
    # Create database directory if it doesn't exist
    if not os.path.exists("database"):
        os.makedirs("database")

    # Connect to the database
    conn = sqlite3.connect("database/business_data.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_intents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_type TEXT,
        intent_name TEXT,
        response_text TEXT,
        training_examples TEXT DEFAULT ''
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_type TEXT UNIQUE,
        default_greeting TEXT,
        default_fallback TEXT,
        enable_voice_support INTEGER DEFAULT 1,
        enable_multilingual INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        business_type TEXT UNIQUE,
        contact_email TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        is_admin INTEGER DEFAULT 0,
        business_id INTEGER,
        FOREIGN KEY (business_id) REFERENCES businesses (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chatbot_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER,
        user_message TEXT,
        bot_response TEXT,
        intent_detected TEXT,
        timestamp TEXT,
        FOREIGN KEY (business_id) REFERENCES businesses (id)
    )
    """)

    # Insert sample data
    sample_business_types = ["retail", "healthcare", "finance"]
    business_data = [
        ("ABC Retail", "retail", "retail@example.com"),
        ("HealthCare Plus", "healthcare", "healthcare@example.com"),
        ("Finance Solutions", "finance", "finance@example.com")
    ]

    for name, business_type, email in business_data:
        cursor.execute("""
        INSERT OR IGNORE INTO businesses (name, business_type, contact_email, is_active)
        VALUES (?, ?, ?, 1)
        """, (name, business_type, email))

    # Insert default bot configurations
    for business_type in sample_business_types:
        cursor.execute("""
        INSERT OR IGNORE INTO bot_config (business_type, default_greeting, default_fallback)
        VALUES (?, ?, ?)
        """, (
            business_type,
            f"Welcome to our {business_type} service! How can I help you today?",
            "I'm not sure I understand. Could you please rephrase your question?"
        ))

    # Insert sample intents and responses
    sample_intents = [
        ("retail", "greet", "Hello! Welcome to our retail store. How can I assist you today?",
         "hi;hello;hey;good morning"),
        ("retail", "goodbye", "Thank you for shopping with us. Have a great day!", "bye;goodbye;see you;later"),
        ("retail", "bot_challenge", "I'm a bot designed to help with retail inquiries.", "are you a bot;are you human"),
        ("retail", "track_order", "I can help you track your order. Please provide your order number.",
         "where is my order;track order;order status"),
        ("retail", "return_policy", "Our return policy allows returns within 30 days of purchase with receipt.",
         "can I return;what's your return policy;how to return"),

        ("healthcare", "greet", "Hello! Welcome to our healthcare service. How can I assist you today?",
         "hi;hello;hey;good morning"),
        ("healthcare", "goodbye", "Take care and stay healthy!", "bye;goodbye;see you;later"),
        ("healthcare", "bot_challenge", "I'm a virtual assistant designed to help with healthcare inquiries.",
         "are you a bot;are you human"),
        ("healthcare", "schedule_appointment",
         "I'd be happy to help you schedule an appointment. What type of specialist do you need to see?",
         "book appointment;schedule appointment;see a doctor"),

        ("finance", "greet", "Hello! Welcome to our financial services. How can I help you today?",
         "hi;hello;hey;good morning"),
        ("finance", "goodbye", "Thank you for using our financial services. Have a great day!",
         "bye;goodbye;see you;later"),
        ("finance", "bot_challenge", "I'm a virtual assistant designed to help with financial inquiries.",
         "are you a bot;are you human"),
        (
        "finance", "open_account", "I can help you open a new account. Would you prefer a checking or savings account?",
        "open account;new account;create account")
    ]

    for business_type, intent_name, response_text, training_examples in sample_intents:
        cursor.execute("""
        INSERT OR IGNORE INTO business_intents (business_type, intent_name, response_text, training_examples)
        VALUES (?, ?, ?, ?)
        """, (business_type, intent_name, response_text, training_examples))

    # Create admin user
    admin_password = generate_password_hash("admin123")
    cursor.execute("""
    INSERT OR IGNORE INTO admin_users (name, email, password, is_admin)
    VALUES (?, ?, ?, 1)
    """, ("Admin User", "admin@example.com", admin_password))

    # Create business users (one for each business type)
    business_user_password = generate_password_hash("password")

    for i, business_type in enumerate(sample_business_types, 1):
        cursor.execute("""
        INSERT OR IGNORE INTO admin_users (name, email, password, is_admin, business_id)
        VALUES (?, ?, ?, 0, ?)
        """, (f"{business_type.capitalize()} User", f"{business_type}@example.com", business_user_password, i))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Database initialized with sample data!")


def install_requirements():
    """Install required Python packages."""
    try:
        # Check if in virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("WARNING: It seems you are not using a virtual environment. It's recommended to use one.")
            response = input("Do you want to continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Exiting. Please create and activate a virtual environment before running this script.")
                sys.exit(1)

        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Required packages installed successfully!")

    except subprocess.CalledProcessError:
        print("Error installing requirements. Please check your requirements.txt file.")
        sys.exit(1)


def update_requirements():
    """Update the requirements.txt file with additional dependencies."""
    # Additional dependencies for Flask app
    additional_deps = [
        "flask",
        "flask-login",
        "werkzeug",
        "wtforms",
        "flask-wtf",
        "alembic",
        "python-dotenv"
    ]

    # Read existing requirements
    with open("requirements.txt", "r") as f:
        existing_reqs = f.read().splitlines()

    # Add new dependencies if not already present
    updated_reqs = existing_reqs.copy()
    for dep in additional_deps:
        if not any(req.startswith(dep) for req in existing_reqs):
            updated_reqs.append(dep)

    # Write updated requirements
    with open("requirements.txt", "w") as f:
        f.write("\n".join(updated_reqs))

    print("requirements.txt updated with additional dependencies!")


def create_flask_app_files():
    """Create the necessary files for Flask app."""
    # Create .env file
    with open(".env", "w") as f:
        f.write("FLASK_APP=app.py\n")
        f.write("FLASK_ENV=development\n")
        f.write("SECRET_KEY=your-secret-key-for-development\n")

    print("Flask app files created!")


def generate_sample_nlu():
    """Generate a sample NLU file from the database."""
    import sqlite3
    import yaml

    conn = sqlite3.connect("database/business_data.db")
    cursor = conn.cursor()

    # Get all intents from the database
    cursor.execute("SELECT intent_name, training_examples FROM business_intents")
    intents_data = cursor.fetchall()

    nlu_data = {"version": "3.1", "nlu": []}

    # Add intents to NLU data
    for intent_name, training_examples in intents_data:
        if training_examples:
            examples = training_examples.split(";")
            nlu_data["nlu"].append({
                "intent": intent_name,
                "examples": "- " + "\n- ".join(examples)
            })

    # Add special intents
    special_intents = [
        {
            "intent": "set_business_type",
            "examples": "- My business type is [healthcare](business_type)\n- I run a [retail](business_type) business\n- I work in [finance](business_type)\n- Change my business type to [healthcare](business_type)"
        },
        {
            "intent": "request_intents",
            "examples": "- What can you do?\n- Show me the available intents\n- List all the things you can help with"
        }
    ]

    for intent in special_intents:
        nlu_data["nlu"].append(intent)

    # Write NLU data to file
    with open("data/nlu.yml", "w") as f:
        yaml.dump(nlu_data, f, allow_unicode=True, default_flow_style=False)

    print("Sample NLU file generated!")


def main():
    """Main function to set up the project."""
    print("Setting up Rasa Customizable Framework...")

    create_directory_structure()
    initialize_database()
    update_requirements()
    create_flask_app_files()

    try:
        generate_sample_nlu()
    except Exception as e:
        print(f"Warning: Could not generate sample NLU file: {e}")

    print("\nProject setup complete!")
    print("\nNext steps:")
    print("1. Activate your virtual environment (if not already)")
    print("2. Install requirements: pip install -r requirements.txt")
    print("3. Start the Flask app: flask run")
    print("4. In a separate terminal, start Rasa actions server: rasa run actions")
    print("5. In another terminal, start Rasa server: rasa run --enable-api")
    print("\nAdmin login:")
    print("Email: admin@example.com")
    print("Password: admin123")


if __name__ == "__main__":
    main()