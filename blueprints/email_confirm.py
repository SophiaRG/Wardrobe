# from flask import Blueprint, jsonify, request
# import mysql.connector
# from main import app, mail
# # from flask_mail import Message
# from utilities.token_required import token_required
# from utilities.db_utilities import confirm_token, convert_db_data_in_list_dict

# e_confirm_bp = Blueprint('email_confirm', __name__)

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="dressMe",
#     password="qwerty54321",
#     database="mydatabase",
# )

# mycursor = mydb.cursor()


# # @e_confirm_bp.route("/confirm/<token>")
# # @token_required
# # def email_confirm(token, user_id):
# #     try:
# #         email = confirm_token(token)
# #     except:
# #         return {
# #                    "message": "The client does not have access rights to the content.",
# #                    "data": None,
# #                    "error": "Forbidden"
# #                }, 403
# #
# #     mycursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
# #
# #     user = convert_db_data_in_list_dict(mycursor)
# #     return user


# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         sender="sophiagorb13@gmail.com"
#     )
#     mail.send(msg)
