from flask import Blueprint, render_template, request, redirect, flash, url_for, json
from MyApp import storage, db
from werkzeug.utils import secure_filename


foods = Blueprint('foods', __name__)

@foods.route('/add_foods')
def add_foods():
    print("add foods called")
    return render_template("foods_add.html")

def downloadUri(image, token):
    imageUri = None
    imageUri = storage.child("Foods/logos/" + secure_filename(image.filename)).get_url(token)
    return imageUri


@foods.route('/add_foods/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        foodName = request.form['foodName']
        foodPrice = request.form['foodPrice']
        foodImage = request.files['foodImage']
        if foodImage and foodName and foodPrice:
            upload = storage.child("Foods/logos/" + secure_filename(foodImage.filename)).put(foodImage)
            filePath = downloadUri(foodImage, upload['downloadTokens'])
            if filePath:
                data = { 'foodName' : foodName, 'foodPrice' : foodPrice, 'foodImageUri' : filePath }
                db.child("Foods").child(foodName).set(data)
                return redirect(url_for("foods.foods_list"))
            else:
                print("File Path Return empty")
        else:
            print("some data field may b empty")

    return render_template("foods_add.html")


@foods.route('/foods_list')
def foods_list():
    tmpData = db.child("Foods").get()
    data = dict(tmpData.val())
    print(data)
    return render_template("foods_list.html", data=data)


def availability(name, condition):
    pair = {'availability' : condition }
    db.child("Foods").child(name).update(pair)

@foods.route('/foods_list/availability', methods=["POST"])
def processAvailability():
    condition = None
    data = { 'status' : 'ok', 'condition' : condition}
    if request.method == 'POST':
        itemName = request.form['itemName']
        con = request.form['condition']
        if con == "true":
            condition = True
        else:
            condition = False
        availability(itemName, condition)
        print(condition)
        data['condition'] = condition 

    return json.dumps(data)