import os
import sys
sys.path.append(os.getcwd())

from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    if admin:
        print(f"Admin found: {admin.username} / {admin.email}")
    else:
        print("No admin user found. Creating one...")
        from app import bcrypt
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@washease.com', password=hashed_password, role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin / admin123")
