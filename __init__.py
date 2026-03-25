import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_name=None):
    flask_app = Flask(__name__)
    
    # Configuration
    flask_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key-12345')
    
    # Absolute path for SQLite database to avoid working directory issues
    basedir = os.path.abspath(os.path.dirname(__file__))
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'washease.db')
        
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail Configuration (must be set BEFORE mail.init_app)
    flask_app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    flask_app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    flask_app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    flask_app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    flask_app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    # Initialize extensions with app
    db.init_app(flask_app)
    bcrypt.init_app(flask_app)
    login_manager.init_app(flask_app)
    mail.init_app(flask_app)

    # Import blueprints (routes)
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.ml import ml_bp
    
    # Register blueprints
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(user_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(ml_bp)
    
    # Ensure instance folder exists for the sqlite database
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    # Create tables on startup
    with flask_app.app_context():
        import app.models # ensure models are imported before creating all
        db.create_all()

    return flask_app
