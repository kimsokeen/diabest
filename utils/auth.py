import sqlite3

def authenticate_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def create_users_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

import sqlite3
import hashlib

# Function to create database connection
def create_connection():
    return sqlite3.connect("users.db")

# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_account(username, password, full_name, age, gender, tel, email):
    conn = create_connection()
    c = conn.cursor()
    try:
        # Ensure users table exists with gender and tel columns
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """)

        hashed_password = hash_password(password)  # Hash password before storing
        c.execute(
            "INSERT INTO users (username, password, full_name, age, gender, tel, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, hashed_password, full_name, age, gender, tel, email),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Error creating account:", e)
        return False


# Function to validate login
def login(username, entered_password):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        if row:
            stored_hashed_password = row[0]
            return hash_password(entered_password) == stored_hashed_password  # Compare hashed passwords
        else:
            return False  # Username not found
    except sqlite3.Error as e:
        print("Error during login:", e)
        return False
    finally:
        conn.close()
