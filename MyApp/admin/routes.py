from flask import Blueprint, render_template, request, flash, redirect,url_for, json, abort
from MyApp import db
from datetime import datetime
from flask_login import login_user, logout_user, login_required
from MyApp.models import User, isConnected

admin = Blueprint('admin', __name__)

@admin.route("/", methods=['GET', 'POST'])
@admin.route("/admin", methods=['GET', 'POST'])
def admin_login():
    email_data = 'shkhaider2015@gmail.com'
    pass_data = '123'
    if request.method == 'POST':
        email_data = request.form['email']
        pass_data = request.form['password']
        print(email_data, pass_data)
        user = User.query.filter_by(email=email_data).first()
        if user and (user.password == pass_data):
            login_user(user, remember=True)
            return redirect(url_for('admin.admin_main'))

        else:
            flash("Unsuccessfull login", 'danger')
    else:
        print("kk")

    return render_template("index.html")


@admin.route("/home")
@login_required
def admin_main():
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    users = db.child("Users").get()
    userList = list()
    if users.val():
        for user in users.each():
            profile = user.val()
            data = profile['Profile']
            print("My data : " + str(data))
            userList.append(data)
    return render_template("admin_home_page.html", users=userList)

@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route("/order")
@login_required
def admin_order():
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    orders = db.child("Orders").get()
    objectList = list()
    for order in orders.each():
        print("Loop Runs ")
        print(order.val())
        objectList.append(dict(order.val()))
    print(objectList)
    objectList.reverse()
    return render_template("admin_order.html", objectList=objectList)


@admin.route("/accept_process", methods=['POST'])
@login_required
def process_accept():
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    data = None
    if request.method == 'POST':
        data = request.form['data']
        user_id = str(data[:-13:1])
        order_id = str(data[-13::1])
        pair = {'accepted' : True}
        print(user_id)
        print(order_id)
        db.child("Orders").child(order_id).update(pair)
        db.child("Users").child(user_id).child("Orders").child(order_id).update(pair)

        return json.dumps({'status':'OK'})
    print("Not a Post Request")


@admin.route("/profile/<string:uid>")
@login_required
def user_profile(uid):
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    profile_path = db.child("Users").child(uid).child("Profile").get()
    orders_path = db.child("Users").child(uid).child("Orders").get()
    profile = dict(profile_path.val())

    if orders_path.val():
        orders = dict(orders_path.val())
    else:
        orders = None
    
    return render_template("profile.html", profile=profile, orders=orders)

