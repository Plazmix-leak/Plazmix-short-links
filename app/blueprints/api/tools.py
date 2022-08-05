import os
from flask import request, jsonify
from functools import wraps


def api_methods(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if os.getenv('API-TOKEN') != api_key:
            return jsonify({"result": False, "error": {"code": 401, "msg": "invalid api key"}})

        return function(*args, **kwargs)

    return wrapper
