from app import create_app, db, bcrypt
from app.models import User
app = create_app()
with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    if admin:
        admin.password = bcrypt.generate_password_hash('123456').decode('utf-8')
        db.session.commit()
        print("Admin password updated to 123456")
    else:
        print("Admin user not found")
