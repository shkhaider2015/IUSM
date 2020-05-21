from flask import Blueprint, render_template, request
from MyApp import storage

foods = Blueprint('foods', __name__)

@foods.route('/add_foods')
def add_foods():
    print("add foods called")
    return render_template("foods_add.html")

def uploadImage(image):
    imageUri = None
    storage.child("foods").child("logos").put(image)
    imageUri = storage.child("foods").child("logos").child(image).get_url()

    if imageUri != None:
        print(imageUri)
    else:
        print("Did Not get Image Uri")


@foods.route('/add_foods/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        foodName = request.form['foodName']
        foodPrice = request.form['foodPrice']
        foodImage = request.form['foodImage']
        uploadImage(foodImage)
        print(foodName, foodPrice, foodImage)
    return render_template("foods_add.html")