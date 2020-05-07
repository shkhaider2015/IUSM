from flask import Blueprint, render_template, request, flash, redirect,url_for, json
from MyApp import db

admin = Blueprint('admin', __name__)

@admin.route("/", methods=['GET', 'POST'])
@admin.route("/admin", methods=['GET', 'POST'])
def admin_login():
    email_data = 'shkhaider2015@gmail.com'
    pass_data = '123'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == email_data and password == pass_data:
            return redirect(url_for('admin.admin_main'))
        else:
            print("Not Matched")
    return render_template("index.html")


@admin.route("/home")
def admin_main():
    users = db.child("Users").get()
    userList = list()
    for user in users.each():
        profile = user.val()
        data = profile['Profile']
        print("My data : " + str(data))
        userList.append(data)
    return render_template("admin_home_page.html", users=userList)

@admin.route("/order")
def admin_order():
    orders = db.child("Orders").get()
    print(type(orders))
    objectList = list()
    for order in orders.each():
        objectList.append(dict(order.val()))
    return render_template("admin_order.html", objectList=objectList)

@admin.route("/accept_process", methods=['POST'])
def process_accept():
    data = None
    if request.method == 'POST':
        data = request.form['data']
        user_id = str(data[:-13:1])
        order_id = str(data[-13::1])
        pair = {'accepted' : True}
        db.child("Orders").child(user_id).child(order_id).update(pair)
        return json.dumps({'status':'OK'})
    print("Not a Post Request")