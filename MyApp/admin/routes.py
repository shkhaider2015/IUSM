from flask import Blueprint, render_template
from MyApp import db

admin = Blueprint('admin', __name__)

@admin.route("/admin")
def admin_login():
    return render_template("index.html")


@admin.route("/home")
def admin_main():
    return render_template("admin_home.html")