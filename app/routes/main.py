from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return "WashEase Full System Running 🚀"
