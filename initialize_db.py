from utils.database import create_connection, create_results_table

# Ensure the `results` table exists
create_results_table()

# Insert dummy data for testing
conn = create_connection()
c = conn.cursor()
c.execute("INSERT INTO results (username, result, wound_size) VALUES (?, ?, ?)", ("test_user", "Positive", 2.5))
conn.commit()
conn.close()

print("Database initialized, and dummy data inserted successfully!")
