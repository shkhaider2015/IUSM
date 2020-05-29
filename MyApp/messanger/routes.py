from flask import Blueprint, render_template, request, flash, redirect,url_for, json, abort
from MyApp import db
import time
from flask_login import login_required
from MyApp.models import isConnected
from datetime import datetime


messanger = Blueprint('messanger', __name__)

previous_data = dict()

def get_data(key):
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    print(key)
    tmp = db.child("Users").child(key).child("Chat").get()
    dicts = dict(tmp.val())
    print(dicts)
    return dicts




@messanger.route("/send_message", methods=['POST'])
@login_required
def message_send():
    data = None
    msg = None
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
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
@login_required
def chat(key):
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    return render_template("chat_jq.html", key=key)

@messanger.route("/accept_chat_process", methods=['POST', 'GET'])
@login_required
def chat_process():
    if not isConnected():
        print("---------------------------Connection Error------------")
        return abort(404, description="Resource not found")
    global previous_data
    key = request.form['key']
    m_type = request.form['m_type']
    data = dict()
    
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
        previous_data = data
        
    elif m_type == 'detect_changes':
        next_data = get_data(key)
        if not bool(previous_data):
            print("Previous Dict is empty")
            previous_data = next_data
            return json.dumps({'status' : 'initialize'})
        else:
            if previous_data == next_data:
                print("Nothing Changes")
                return json.dumps({'status' : 'nothing changed'})
            else:
                data = next_data
                previous_data = next_data
                print("Somthing changes")
    elif m_type == "refresh":
        data = get_data(key)
        previous_data = data


    
    
    return json.dumps(data)
