from functools import wraps
from jwt import decode
from flask import request
from dotenv import load_dotenv
import os

load_dotenv()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                       "message": "Authentication Token is missing!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        try:
            data = decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
            user_id = data["user_id"]
        except:
            return {
                       "message": "Authorization went wrong",
                       "data": None,
                       "error": "Invalid token"
                   }, 400
        return f(user_id, *args, **kwargs)

    return decorated
