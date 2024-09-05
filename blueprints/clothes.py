from flask import Blueprint, jsonify, request
import requests
import mysql.connector
from utilities.token_required import token_required
from utilities.db_utilities import list_of_clothes_by_temp, select_from_other_to_final_dict
import random
import os
from dotenv import load_dotenv

clothes_bp = Blueprint('clothes', __name__)

mydb = mysql.connector.connect(
    host=os.environ['MYSQL_DATABASE_HOST'],
    user=os.environ['MYSQL_DATABASE_USERNAME'],
    password=os.environ['MYSQL_DATABASE_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
)

mycursor = mydb.cursor()

load_dotenv()

clothes_classifications = {
    "top": ["T-shirt", "shirt", "sweater", "hoodie", "light sweater", "crop top", "polo", "top"],
    "dress": ["summer dress", "night dress", "long dress", "warm dress"],
    "bottom": ["shorts", "jeans", "casual pants"],
    "shoes": ["trainers", "heels", "boots", "keds"],
    "coat": ["bomber jacket", "warm coat", "denim jacket", "jacket", "overcoat", "vest"],
    "other": ["umbrella", "sun glasses", "gloves", "scarf"]
}


@clothes_bp.route("/all_clothes_by_weather")
@token_required
def all_clothes_by_weather(user_id):
    response = requests.get(url=os.environ['API_CALL'])
    response.raise_for_status()
    data = response.json()

    temp_now = int(data["main"]["temp"])

    args = request.args
    temp_request = args.get("temp", default=temp_now, type=int)
    class_request = args.get("classification", type=str)

    if temp_request:
        temp = temp_request
    else:
        temp = temp_now

    list_of_clothes = list_of_clothes_by_temp(mycursor, user_id, temp)

    # checks if there were requested query parameters for clothes classification.
    # if yes then it will be randomly chosen from these clothes
    clothes_classifications_requested = {}

    if class_request:
        class_request = class_request.split("+")
        classification_requested_list = class_request[0].split(" ")

        try:
            for i in range(len(classification_requested_list)):
                key = classification_requested_list[i]
                clothes_classifications_requested[key] = clothes_classifications[key]
        except:
            return {
                       "message": "Cannot find requested classification.",
                       "data": None,
                       "error": "Does not exist."
                   }, 404

        target_classification = clothes_classifications_requested
    else:
        target_classification = clothes_classifications

    # Creating list with clothes sorted by classifications: top, bottom, dress, coat, shoes, other, all;
    # Or creating list with requested clothes from query params

    dictionary_by_classes = {}

    for classification in target_classification:
        list_of_items = []
        count = 0
        for item in list_of_clothes:
            if item['type'] in target_classification[classification]:
                list_of_items.append(item)
                count += 1
        if count == 0:
            dictionary_by_classes[classification] = ["No item available"]
        else:
            dictionary_by_classes[classification] = list_of_items

    return dictionary_by_classes


@clothes_bp.route("/random_clothes_by_weather", methods=['GET'])
@token_required
def random_clothes_by_weather(user_id):
    response = requests.get(url=os.environ['API_CALL'])
    response.raise_for_status()
    data = response.json()

    weather_description = data["weather"][0]["description"]
    temp_now = int(data["main"]["temp"])

    # query params (temp + classification); in format "http://127.0.01:5000...?temp=10&classification=top+bottom"
    args = request.args
    temp_request = args.get("temp", default=temp_now, type=int)
    class_request = args.get("classification", type=str)

    if temp_request:
        temp = temp_request
    else:
        temp = temp_now

    list_of_clothes = list_of_clothes_by_temp(mycursor, user_id, temp)

    # checks if there were requested query parameters for clothes classification.
    # if yes then it will be randomly chosen from these clothes
    clothes_classifications_requested = {}
    if class_request:
        class_request = class_request.split("+")
        classification_requested_list = class_request[0].split(" ")

        try:
            key = None
            for i in range(len(classification_requested_list)):
                key = classification_requested_list[i]
                clothes_classifications_requested[key] = clothes_classifications[key]
        except:
            return {
                        "message": f"Cannot find requested classification: {key}.",
                        "data": None,
                        "error": "Does not exist."
                       }, 404

        target_classification = clothes_classifications_requested
    else:
        target_classification = clothes_classifications

    dictionary_by_classes = {}
    for classification in target_classification:
        list_of_items = []
        count = 0
        for item in list_of_clothes:
            if item['type'] in target_classification[classification]:
                list_of_items.append(item)
                count += 1
        if count == 0:
            dictionary_by_classes[classification] = ["No item available"]
        else:
            dictionary_by_classes[classification] = list_of_items

    # creating final list of clothes by random choice
    # spring, summer, autumn, spring/autumn, winter, all, other - types of seasons
    # ALL season means it can be worn all year
    # if it's rain or sun (getting this type of information from weather description) we are adding an
    # umbrella or sunglasses accordingly (in database they are in OTHER season, in dictionary OTHER)

    final_dict_to_dress = {}

    for clothes in dictionary_by_classes:
        choice = random.choice(dictionary_by_classes[clothes])
        final_dict_to_dress[clothes] = choice

    if target_classification == clothes_classifications:
        if "rain" in weather_description:
            select_from_other_to_final_dict("umbrella", dictionary_by_classes, final_dict_to_dress)
        elif "sun" in weather_description:
            select_from_other_to_final_dict("sunglasses", dictionary_by_classes, final_dict_to_dress)

    return final_dict_to_dress

# TODO: decide what is better: temp now or temp max of the day
# TODO: there is an idea to check difference between min and max temps to check if coat in spring/autumn is needed.
# cold: temp >0
# normal (spring/autumn) : 0< temp >15
# summer: temp >15
