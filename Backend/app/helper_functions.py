from .models import Mobilizer, OperationManager, Students, CustomToken
import jwt
import os
import datetime
import requests
from dotenv import load_dotenv
load_dotenv()


def get_object(token):
    try:
        token = token.split(" ")
        print(token)
        payload = jwt.decode(token[1], os.getenv(
            'JWT_SECRET'), algorithms=['HS256'])
        print(payload)
        if payload['user_type'] == 0:
            # Operations Manager
            print(payload['id'])
            required_object = list(OperationManager.objects.filter(id=payload['id']))[
                0]
        else:
            # Mobilizer
            required_object = list(
                Mobilizer.objects.filter(id=payload['id']))[0]
            pass
        token = list(CustomToken.objects.filter(
            object_id=required_object.id, user_type=payload['user_type']))[0]
        return required_object
    except Exception as error:
        print(error)
        return None


def get_token(object_id, user_type):
    payload = {
        'user_type': user_type,
        'id': object_id,
        'time_stamp': str(datetime.datetime.today())
    }
    encoded_jwt = jwt.encode(payload, os.getenv(
        'JWT_SECRET'), algorithm='HS256')
    result = (encoded_jwt.decode("utf-8"))
    return result


def check_user(token):
    try:
        token = token.split(" ")
        payload = jwt.decode(token[1], os.getenv(
            'JWT_SECRET'), algorithms=['HS256'])
        return payload['user_type']
    except Exception as error:
        print(error)
        return None
