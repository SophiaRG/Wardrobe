from datetime import datetime
import random
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv


def convert_db_data_in_list_dict(mycursor):
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    list_of_clothes = []
    for list in myresult:
        clothes_dictionary = {}
        for index in range(len(field_names)):
            clothes_dictionary[field_names[index]] = list[index]
        list_of_clothes.append(clothes_dictionary)

    return list_of_clothes


def add_clothes_by_season_to_list(mycursor, user_id, season):
    try:
        mycursor.execute(f"SELECT * FROM clothes WHERE user_id = %s AND season = '{season}'", (user_id,))
    except:
        return {
            "message": "No such season.",
            "data": None,
            "error": "Incorrect season"
        }, 404
    return convert_db_data_in_list_dict(mycursor)


def list_of_clothes_by_temp(mycursor, user_id, temp):
    month = datetime.now().month
    list_of_clothes = []
    if temp <= 0:
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'winter')
    elif 0 < temp <= 15 and 2 < month < 6:
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'spring/autumn')
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'spring')
    elif 0 < temp <= 15 and 8 < month < 12:
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'spring/autumn')
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'autumn')
    elif temp > 15:
        list_of_clothes += add_clothes_by_season_to_list(mycursor, user_id, 'summer')

    mycursor.execute("SELECT * FROM clothes WHERE user_id = %s AND season = 'all'", (user_id,))
    list_of_clothes += convert_db_data_in_list_dict(mycursor)
    mycursor.execute("SELECT * FROM clothes WHERE user_id = %s AND season = 'other'", (user_id,))
    list_of_clothes += convert_db_data_in_list_dict(mycursor)
    return list_of_clothes


def select_from_other_to_final_dict(type, dictionary_by_classes, final_dict):
    item_from_other = [item for item in dictionary_by_classes["other"] if item["type"] == type]
    item_from_other = random.choice(item_from_other)
    final_dict[type] = item_from_other
    return final_dict


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])
    return serializer.dumps(email, salt='SECURITY_PASSWORD_SALT')


def confirm_token(token, salted_password, expiration=3600):
    serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=salted_password,
            max_age=expiration
        )
    except:
        return False
    return email
