from flask import Blueprint, render_template, request, flash, redirect,url_for, json
from MyApp import db
from datetime import datetime

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
    objectList = list()
    for order in orders.each():
        print("Loop Runs ")
        print(order.val())
        objectList.append(dict(order.val()))
    print(objectList)
    objectList.reverse()
    return render_template("admin_order.html", objectList=objectList)

@admin.route("/accept_process", methods=['POST'])
def process_accept():
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
def user_profile(uid):
    profile_path = db.child("Users").child(uid).child("Profile").get()
    orders_path = db.child("Users").child(uid).child("Orders").get()
    profile = dict(profile_path.val())
    orders = dict(orders_path.val())
    
    return render_template("profile.html", profile=profile, orders=orders)

@admin.route("/messaging")
def chat():
    data = db.child("Chat").get()
    data = dict(data.val())
    user_msg = dict()
    for k,v in data.items():
        if v['senderId'] not in user_msg:
            user_msg[v['senderId']] = {k:v}
        else:
            user_msg[v['senderId']].update({k:v})
    side_bar = list()
    for k,v in user_msg.items():
        for kk,vv in v.items():
            side_bar.append({kk:vv})
            break
    side_bar.reverse()
    first_person = side_bar[0]
    for k,v in first_person.items():
        first_person = v
    first_person_data = db.child("Users").child(first_person['senderId']).child("Chat").get()
    first_person_data = dict(first_person_data.val())
    
    return render_template("chat_room.html", first_person_data=first_person_data, side_bar=side_bar, senderID=first_person['senderId'])

@admin.route("/send_message", methods=['POST'])
def message_send():
    data = None
    msg = None
    if request.method == 'POST':
        time = datetime.now().timestamp() * 1000
        data = request.form['data']
        msg = request.form['msg']
        senderid = request.form['senderid']
        if data == 'admin' and msg != None:
            print("Admin Call")
            pushData = { 
                'senderId' : "17352015",
                'senderName' : "Admin",
                'senderEmail' : "admin@gmail.com",
                'senderProfileUri' : str("https://firebasestorage.googleapis.com/v0/b/canteen-management-syste-e183d.appspot.com/o/Admin%2Fburger.png?alt=media&token=b6731782-c9a6-452a-8bb6-46a4ce8a8321"),
                'msgTime' : time,
                'msg' : msg}

            db.child("Users").child(senderid).child("Chat").child(time).push(pushData)
            
        else:
            print("Another Call")
        return json.dumps({'status' : 'ok'})
    print("Not a post Request")

