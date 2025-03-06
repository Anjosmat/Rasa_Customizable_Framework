import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create table for intents and responses
cursor.execute("""
CREATE TABLE IF NOT EXISTS intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_name TEXT UNIQUE,
    response TEXT
)
""")

# Create table for bot configurations (optional, for future features)
cursor.execute("""
CREATE TABLE IF NOT EXISTS bot_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting TEXT UNIQUE,
    value TEXT
)
""")

# Insert some sample responses (prevent duplicates)
intents_data = [
    ('greet', 'Hello! How can I assist you today?'),
    ('goodbye', 'Goodbye! Have a great day!'),
    ('bot_challenge', 'I am a bot, powered by Rasa.')
]

cursor.executemany("INSERT OR IGNORE INTO intents (intent_name, response) VALUES (?, ?)", intents_data)

# Commit and close
conn.commit()
conn.close()

print("Database setup complete.")
