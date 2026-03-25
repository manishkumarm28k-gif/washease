import os
import sys
# Add current directory to path so app can be imported
sys.path.append(os.getcwd())

from app import create_app, db
from app.models import Franchise
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    if 'franchise' not in inspector.get_table_names():
        print("Table 'franchise' does not exist. Creating it now...")
        db.create_all()
        print("Table 'franchise' created.")
    else:
        print("Table 'franchise' already exists.")
        
    # Check if there's any data
    count = Franchise.query.count()
    print(f"Total franchise inquiries: {count}")
