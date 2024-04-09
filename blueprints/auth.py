from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from utilities.db_utilities import convert_db_data_in_list_dict, generate_confirmation_token, confirm_token
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
auth_bp = Blueprint('auth', __name__)

mydb = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE'],
)

mycursor = mydb.cursor()


@auth_bp.route("/register", methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        try:
            username = request.json.get("username")
            email = request.json.get("email")
            password = request.json.get("password")
        except:
            return {
                       "message": "Invalid request data!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 400

        mycursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = mycursor.fetchone()

        if account:
            return {
                       "message": "Account already exist!",
                       "data": None,
                       "error": "Conflict"
                   }, 409
        else:
            hash_and_salted_password = generate_password_hash(
                password,
                method="pbkdf2:sha256",
                salt_length=8
            )

        confirmed = False
        token = generate_confirmation_token(email)
        print(token)

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        new_user = (username, email, hash_and_salted_password)
        mycursor.execute(sql, new_user)
        mydb.commit()

        return jsonify({"Message": "You successfully registered."}), 201

    return jsonify({"Message": "Register or login first."}), 200


@auth_bp.route('/login', methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        try:
            email = request.json.get("email")
            password = request.json.get("password")
        except:
            return {
                       "message": "Invalid request message!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 400
        try:
            mycursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        except:
            return {
                       "message": "Cannot find requested user.",
                       "data": None,
                       "error": "Does not exist."
                   }, 404
        user = convert_db_data_in_list_dict(mycursor)
        ps_hash = str(user[0]["password"])
        user_id = str(user[0]["user_id"])
        if user and check_password_hash(ps_hash, password=password):
            access_token = jwt.encode({'email': email, "user_id": user_id}, key=os.environ['SECRET_KEY'])
            print(access_token)
            return jsonify(
                {
                    "message": "Logged in",
                    "token": {
                        "access": access_token,
                    }
                }
            ), 200

    return jsonify({"Message": "Register or login first."}), 200


