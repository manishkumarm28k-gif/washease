import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)
