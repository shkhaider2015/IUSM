from flask import Blueprint
from MyApp import db

admin = Blueprint('admin', __name__)

@admin.route("/admin")
def admin_home():
    db.child("admin").push({"name":"shakeel"})
    return "Hello Admin"
