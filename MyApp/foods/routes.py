from flask import Blueprint, render_template, request
from MyApp import storage, db
from werkzeug.utils import secure_filename


foods = Blueprint('foods', __name__)

@foods.route('/add_foods')
def add_foods():
    print("add foods called")
    return render_template("foods_add.html")

def downloadUri(image):
    imageUri = None
    imageUri = storage.child("foods/logos/" + secure_filename(image.filename)).get_url(None)
    return imageUri


@foods.route('/add_foods/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        foodName = request.form['foodName']
        foodPrice = request.form['foodPrice']
        foodImage = request.files['foodImage']
        if foodImage and foodName and foodPrice:
            storage.child("Foods/logos/" + secure_filename(foodImage.filename)).put(foodImage)
            filePath = downloadUri(foodImage)
            if filePath:
                data = { 'foodName' : foodName, 'foodPrice' : foodPrice, 'foodImageUri' : filePath }
                db.child("Foods").child(foodName).set(data)
            else:
                print("File Path Return empty")
        else:
            print("some data field may b empty")

    return render_template("foods_add.html")