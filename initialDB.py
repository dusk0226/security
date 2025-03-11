import sqlite3
import os

def init_db():
    """Creates the SQLite database and inserts multiple users."""      
    # **Delete the existing database file**
    if os.path.exists("bank.db"):
        os.remove("bank.db")
        print("Old database deleted.")

    # **Create a fresh connection**
    conn = sqlite3.connect("bank.db")  # Connect to the new SQLite database
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
    ''')

    # Create Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            amount REAL,
            timestamp TEXT,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    ''')

    # Insert users into the database
    users_data = [
        (1001, 'member1', 'pass1', 'wk20230401@outlook.com', 50.0),
        (1002, 'member2', 'pass2', 'wk20230401@outlook.com', 500.0),
        (1003, 'member3', 'pass3', 'wk20230401@outlook.com', 1000.0),
        (1004, 'member4', 'pass4', 'wk20230401@outlook.com', 120.0),       
    ]

    # Insert users, ignore if they already exist
    cursor.executemany("INSERT OR IGNORE INTO users (id, username, password, email, balance) VALUES (?, ?, ?, ?, ?)", users_data)

    conn.commit()
    conn.close()
    print("Database initialized with 4 users.")

# Initialize the database 
init_db()