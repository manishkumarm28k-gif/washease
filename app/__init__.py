from flask import Flask

def create_app():
    app = Flask(__name__)

    # basic config
    app.config['SECRET_KEY'] = 'secret123'

    # simple test route (IMPORTANT)
    @app.route("/")
    def home():
        return "WashEase Full App Running 🚀"

    return app
