import sqlite3
conn = sqlite3.connect('predictions.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    food_type TEXT,
    country TEXT,
    description TEXT,
    confidence REAL,
    nutrients TEXT,
    inference_time REAL,  -- Changed from TEXT to REAL for numerical calculations
    image_processing_time REAL,  -- New column for image processing time
    total_execution_time REAL,  -- New column for total execution time
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               role TEXT,
               name TEXT,
               email TEXT,
               password TEXT
               )
""")

conn.commit()
conn.close()

print("Database and table initialized successfully.")
