from flask import Blueprint, render_template, request, flash, redirect,url_for, json
from MyApp import db
import time

messanger = Blueprint('messanger', __name__)


def get_data(key):
    print(key)
    tmp = db.child("Users").child(key).child("Chat").get()
    dicts = dict(tmp.val())
    print(dicts)
    return dicts



@messanger.route("/messaging/<string:key>", methods=['POST', 'GET'])
def chat(key):
    data = get_data(key)
    print(data)
    return render_template("chat_room.html", data=data)

@messanger.route("/send_message", methods=['POST'])
def message_send():
    data = None
    msg = None
    if request.method == 'POST':
        time = int(datetime.now().timestamp()) * 1000
        data = request.form['data']
        msg = str(request.form['msg'])
        senderid = request.form['senderid']
        image_path =  "https://firebasestorage.googleapis.com/v0/b/canteen-management-syste-e183d.appspot.com/o/Admin%2Fburger.png?alt=media&token=b6731782-c9a6-452a-8bb6-46a4ce8a8321"
        if data == 'adminn' and msg != None:
            print("Admin Call")
            pushData = dict({ 
                'senderId' : "17352015",
                'senderName' : "Admin",
                'senderEmail' : "admin@gmail.com",
                'senderProfileUri' : image_path,
                'msgTime' : time,
                'msg' : msg
                })

            print(f"The Sender Id : {senderid} and time : {time} ")
            db.child("Users").child(senderid).child("Chat").child(time).set(pushData)
            return json.dumps({'status' : 'ok'})
            
        elif data == "page":
            return json.dumps(get_data(senderid))
        else:
            print("Another Call")
            
        return json.dumps({'status' : 'ok'})
    print("Not a post Request")

@messanger.route("/chat/<string:key>", methods=['POST', 'GET'])
def chat_jq(key):
    return render_template("chat_jq.html", key=key)

@messanger.route("/accept_chat_process", methods=['POST', 'GET'])
def chat_process():
    key = request.form['key']
    m_type = request.form['m_type']
    
    if m_type == 'send':
        print("send request")
        msg = request.form['msg']
        msgTime = int(time.time()) * 1000
        set_data = {
            'senderName' : 'admin',
            'senderId' : '17352015',
            'senderEmail' : 'admin@gmail.com',
            'senderProfileUri' : 'https://firebasestorage.googleapis.com/v0/b/canteen-management-syste-e183d.appspot.com/o/Admin%2Fburger.png?alt=media&token=b6731782-c9a6-452a-8bb6-46a4ce8a8321',
            'msgTime' : msgTime,
            'msg' : msg
        }
        db.child("Users").child(key).child("Chat").child(msgTime).set(set_data)
    
    data = get_data(key)
    return json.dumps(data)
