import mysql.connector
from flask import Flask, jsonify, render_template, request
# from flask_mail import Mail
import random
from utilities.db_utilities import convert_db_data_in_list_dict
from blueprints.auth import auth_bp
from blueprints.clothes import clothes_bp
from utilities.token_required import token_required
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# mail = Mail(app)

mydb = mysql.connector.connect(
    host=os.environ['MYSQL_DATABASE_HOST'],
    user=os.environ['MYSQL_DATABASE_USERNAME'],
    password=os.environ['MYSQL_DATABASE_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
)

mycursor = mydb.cursor()

# use_db = f"USE {os.environ(['DB_DATABASE'])};"

mysql_request_clothes_table = "CREATE TABLE IF NOT EXISTS clothes (\
    id INT AUTO_INCREMENT PRIMARY KEY,\
    season VARCHAR(50) NOT NULL,\
    type VARCHAR(50) NOT NULL,\
    classification VARCHAR(70) NOT NULL,\
    colour VARCHAR(50) NOT NULL,\
    user_id INT NOT NULL\
);"

mysql_request_users_table = "CREATE TABLE IF NOT EXISTS users (\
    user_id INT AUTO_INCREMENT PRIMARY KEY,\
    email VARCHAR(255) NOT NULL,\
    username VARCHAR(255) NOT NULL,\
    password VARCHAR(255) NOT NULL\
);"


# mycursor.execute(use_db)
mycursor.execute(mysql_request_clothes_table)
mycursor.execute(mysql_request_users_table)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(clothes_bp, url_prefix="/clothes")


# TODO: create home page with register and login
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/clothes")
@token_required
def get_all(user_id):
    try:
        mycursor.execute("SELECT * FROM clothes WHERE user_id = %s", (user_id,))
    except:
        return {
                   "message": "No clothes yet.",
                   "data": None,
               }, 204
    list_of_clothes = convert_db_data_in_list_dict(mycursor)
    return jsonify(list_of_clothes)


@app.route("/random")
@token_required
def get_random(user_id):
    try:
        mycursor.execute("SELECT * FROM clothes WHERE user_id = %s", (user_id,))
    except:
        return {
                   "message": "No clothes yet.",
                   "data": None,
               }, 204
    list_of_clothes = convert_db_data_in_list_dict(mycursor)
    random_clothes = random.choice(list_of_clothes)
    return jsonify(random_clothes)


# debug function
@app.route("/header")
def headers():
    return jsonify({"message": "answer in print"})


@app.route("/<int:id>")
@token_required
def search_by_index(user_id, id):
    try:
        mycursor.execute(f"SELECT * FROM clothes WHERE user_id = %s AND id = %s", (user_id, id))
    except:
        return {
                   "message": "No such id.",
                   "data": None,
                   "error": "Incorrect id"
               }, 404
    list_of_clothes = convert_db_data_in_list_dict(mycursor)

    return jsonify(list_of_clothes[0])


@app.route("/add", methods=["GET", "POST"])
@token_required
def add(user_id):
    if request.method == "POST":
        try:
            season = request.json.get("season")
            type = request.json.get("type")
            colour = request.json.get("colour")
        except:
            return {
                       "message": "Not all parameters were added.",
                       "data": None,
                       "error": "Bad request"
                   }, 400
        sql = "INSERT INTO clothes (season, type, colour, user_id) VALUES (%s, %s, %s, %s)"
        val = (season, type, colour, user_id)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"Message": "new item was added."}), 201
    return jsonify({"Add new clothes": "In this endpoint you can add new items to your wardrobe."}), 200


@app.route("/delete/<int:id>", methods=["DELETE"])
@token_required
def delete(user_id, id):
    if request.method == "DELETE":
        try:
            mycursor.execute(f"DELETE FROM clothes WHERE user_id = %s AND id = %s", (user_id, id))
        except:
            return {
                       "message": "No such id.",
                       "data": None,
                       "error": "Incorrect id"
                   }, 404
        mydb.commit()
        return jsonify({"Message": "item was deleted."})
    return jsonify({"Delete": "In this endpoint you can delete items from your wardrobe."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
