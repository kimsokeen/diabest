import sqlite3
import datetime
import os
import sqlite3
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

import sqlite3
import os
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def create_results_table():
    try:
        db_path = os.path.abspath("users.db")
        print(f"[DEBUG] Connecting to database at: {db_path}")

        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()

        print("[DEBUG] Creating 'results' table if it does not exist...")

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                result TEXT NOT NULL,
                wound_size REAL NOT NULL,
                overlay_resized BLOB
            )
        """)

        conn.commit()
        print("[DEBUG] 'results' table created or already exists.")
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to create results table: {e}")
    finally:
        if conn:
            conn.close()
            print("[DEBUG] Database connection closed.")


def get_results_by_date(username, selected_date):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT timestamp, result, wound_size, overlay_resized 
            FROM results 
            WHERE username = ? AND timestamp LIKE ?
        """, (username, f"{selected_date}%"))

        results = []
        for row in cursor.fetchall():
            timestamp, result, wound_size, overlay_resized_blob = row

            # ✅ Convert binary data back to an image
            overlay_resized = None
            if overlay_resized_blob:
                # Convert blob to numpy array
                image_array = np.frombuffer(overlay_resized_blob, dtype=np.uint8)

                # Decode image using OpenCV
                overlay_resized = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                # Ensure the image was decoded successfully (not empty)
                if overlay_resized is not None and overlay_resized.size > 0:
                    #overlay_resized = cv2.cvtColor(overlay_resized, cv2.COLOR_BGR2RGB)  # Convert to RGB
                    overlay_resized = Image.fromarray(overlay_resized)  # Convert to PIL Image
                else:
                    print("Warning: Image decoding failed, skipping.")

            results.append((timestamp, result, wound_size, overlay_resized))

        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def get_latest_results(username, limit=5):
    """
    Fetch the latest analysis results from the database for the given username.

    Parameters:
    - username: The username whose results we want to fetch.
    - limit: The number of latest results to retrieve (default is 5).

    Returns:
    - A list of tuples containing (timestamp, result, wound_size) or None if no results are found.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()

        # Query to fetch the latest results for the given username
        cursor.execute("""
            SELECT timestamp, result, wound_size 
            FROM results 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (username, limit))

        # Fetch the results
        results = cursor.fetchall()

        # Close the connection
        conn.close()

        # If there are no results, return None
        if not results:
            return None

        # Return the results as a list of tuples
        return results

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


    """
def create_connection():
    "
    Create and return a connection to the SQLite database.
    ""
    db_path = check_database_path()
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    """

def create_connection():
    return sqlite3.connect('users.db', check_same_thread=False)

def get_user_info(username):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT full_name, age, gender, tel, email FROM users WHERE username = ?", (username,))
        info = c.fetchone()
        conn.close()
        return info  # Now returns full_name, age, gender, tel
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def check_database_path():
    print("Current working directory:", os.getcwd())  # Check where Streamlit runs
    db_path = os.path.abspath("users.db")
    print("Database path:", db_path)
    return db_path

import streamlit as st  # add this if not already

def create_users_table():
    try:
        conn = create_connection()
        if conn is not None:
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



