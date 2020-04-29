from flask import Blueprint, render_template, request, flash
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
            users = db.child("Users").get()
            userList = list()
            for user in users.each():
                profile = user.val()
                data = profile['Profile']
                print("My data : " + str(data))
                userList.append(data)
            return render_template('admin_home.html', users=userList)
        else:
            print("Not Matched")
    users_1 = db.child("Users").get()
    for user in users_1.each():
        val= user.val()
        data = val['Profile']
        print(data)
        name = data['name']
        print(name)
        

    return render_template("index.html")


@admin.route("/home")
def admin_main():
    return render_template("admin_home.html")