import sqlite3
import os
import bcrypt

def seed_db():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'washease.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables manually for initialization if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL, 
        username VARCHAR(20) NOT NULL, 
        email VARCHAR(120) NOT NULL, 
        password VARCHAR(128) NOT NULL, 
        role VARCHAR(10) NOT NULL, 
        is_premium BOOLEAN NOT NULL DEFAULT 0,
        hostel_room VARCHAR(100),
        contact_no VARCHAR(15),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service (
        id INTEGER NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        description TEXT, 
        base_price FLOAT NOT NULL, 
        shop_id INTEGER NOT NULL,
        active BOOLEAN NOT NULL DEFAULT 1,
        PRIMARY KEY (id),
        FOREIGN KEY(shop_id) REFERENCES shop (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shop (
        id INTEGER NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        location VARCHAR(200) NOT NULL, 
        phone VARCHAR(20), 
        rating FLOAT DEFAULT 5.0,
        latitude FLOAT,
        longitude FLOAT,
        serviceable_pincodes VARCHAR(500) DEFAULT '110001,110002',
        PRIMARY KEY (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "order" (
        id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        shop_id INTEGER,
        coupon_id INTEGER,
        tracking_code VARCHAR(40) NOT NULL,
        date_posted DATETIME NOT NULL, 
        status VARCHAR(20) NOT NULL, 
        total_price FLOAT NOT NULL, 
        pickup_address VARCHAR(255) NOT NULL, 
        pickup_date VARCHAR(20) NOT NULL, 
        pickup_time VARCHAR(20) NOT NULL, 
        special_instructions TEXT, 
        items_json TEXT NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (tracking_code),
        FOREIGN KEY(user_id) REFERENCES user (id),
        FOREIGN KEY(shop_id) REFERENCES shop (id),
        FOREIGN KEY(coupon_id) REFERENCES coupon (id)
    )
    ''')

    # Seed Shops (Greater Noida)
    cursor.execute("SELECT COUNT(*) FROM shop")
    if cursor.fetchone()[0] == 0:
        shops = [
            ('WashEase Pari Chowk', 'Pari Chowk, Greater Noida', '9876543210', 4.8, 28.4671, 77.5113, '201308,201310,110001'),
            ('WashEase Knowledge Park', 'Knowledge Park III, Greater Noida', '9876543211', 4.9, 28.4722, 77.4912, '201310,201312,110001'),
            ('WashEase Gamma', 'Gamma 1, Greater Noida', '9876543212', 4.7, 28.4901, 77.5211, '201308,201306,110002'),
            ('WashEase Alpha', 'Alpha 2, Greater Noida', '9876543213', 4.6, 28.4812, 77.5011, '201308,201307,110002')
        ]
        cursor.executemany("INSERT INTO shop (name, location, phone, rating, latitude, longitude, serviceable_pincodes) VALUES (?, ?, ?, ?, ?, ?, ?)", shops)

    # Seed Users
    admin_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT OR IGNORE INTO user (username, email, password, role) VALUES (?, ?, ?, ?)",
                   ('admin', 'admin@washease.com', admin_pw, 'admin'))
                   
    user_pw = bcrypt.hashpw(b"user123", bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT OR IGNORE INTO user (username, email, password, role) VALUES (?, ?, ?, ?)",
                   ('johndoe', 'john@example.com', user_pw, 'user'))
                   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_item (
        id INTEGER NOT NULL, 
        order_id INTEGER NOT NULL, 
        service_id INTEGER NOT NULL, 
        garment_type VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL, 
        unit_price FLOAT NOT NULL, 
        sub_total FLOAT NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(order_id) REFERENCES "order" (id),
        FOREIGN KEY(service_id) REFERENCES service (id)
    )
    ''')
    
    # Seed Services (Rupee Pricing)
    cursor.execute("DELETE FROM service") # Refresh services
    services = [
        ('Wash & Fold', 'Everyday casual clothes washed and neatly folded.', 50.00, 1),
        ('Dry Cleaning', 'Specialized cleaning for delicate fabrics and suits.', 200.00, 1),
        ('Steam Ironing', 'Professional pressing for crisp, wrinkle-free clothes.', 30.00, 1),
        ('Express', 'Fast-track service for urgent laundry needs.', 150.00, 1),
        ('Premium Care', 'Special gentle wash with premium fabric softeners.', 300.00, 1)
    ]
    cursor.executemany("INSERT INTO service (name, description, base_price, shop_id) VALUES (?, ?, ?, ?)", services)
        
    conn.commit()
    conn.close()
    print(f"Database successfully re-seeded at {db_path} with Greater Noida shops and Rupee pricing.")

if __name__ == '__main__':
    seed_db()
