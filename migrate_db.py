import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'washease.db')
    if not os.path.exists(db_path):
        print("Database does not exist. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Add is_premium column to user table
        cursor.execute("ALTER TABLE user ADD COLUMN is_premium BOOLEAN DEFAULT 0 NOT NULL")
        print("Added is_premium column to user table.")
    except sqlite3.OperationalError as e:
        print(f"is_premium column error: {e}")

    try:
        # Add hostel_room column to user table
        cursor.execute("ALTER TABLE user ADD COLUMN hostel_room VARCHAR(100)")
        print("Added hostel_room column to user table.")
    except sqlite3.OperationalError as e:
        print(f"hostel_room column error: {e}")

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == '__main__':
    migrate()
