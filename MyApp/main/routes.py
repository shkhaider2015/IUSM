from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/ho")
def home():
    return "Welcome home"