import datetime
from enum import Enum

import redis
from mongoengine import *
import string
import random


# Tables
#     - User
#     _ Purchase
#     - Payee
#     - Activity
#     - User Credentials
#     - Payee Credentials


def getID():
    temp = ''.join(random.choices(string.ascii_lowercase +
                                  string.digits, k=14))
    return temp


class RedisInstance:
    redis_instance = None

    def __init__(self):
        self.redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=0)


redis_instance = RedisInstance().redis_instance


def init_database_connection():
    connect(db="CardUp", host="54.202.248.205", port=27017, username="saurabh", password="Imsaurabh@1",
            authentication_source="admin")


class Gender(Enum):
    female = 'female'
    male = 'male'
    other = 'other'


class ActivityOptions(Enum):
    login = "login"
    signin = "signin"
    purchase = "purchase"
    resource_access = "resource_access"


class User(Document):
    user_id = StringField(required=True)
    username = StringField(required=False, max_length=30)
    password = StringField(required=False, max_length=100, min_length=8,
                           regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    name = StringField(required=False, max_length=30)
    gender = EnumField(required=False, enum=Gender, default=Gender.other)
    dob = DateField(required=False)
    phone_number = StringField(required=False, max_length=13)
    email = EmailField(required=False)
    kyc_id = StringField(required=False)
    kyc_status = BooleanField(required=False, default=False)
    user_timestamp = DateTimeField(required=True)


class Purchase(Document):
    user_id = StringField(required=True, max_length=100)
    purchase_id = StringField(required=False, default="P__" + getID())
    machine_id = StringField(required=True, max_length=32)
    amount = IntField(required=True)
    self_profit = IntField(required=True)
    payee_profit = IntField(required=True)
    website = StringField(required=True)
    item_name = StringField(required=False)
    payee_id = StringField(required=True)
    lat = StringField(required=True)
    long = StringField(required=True)


class UserCredential(Document):
    machine_id = StringField(required=True, max_length=100)
    user_id = StringField(required=True)
    access_token = StringField(required=False)
    refresh_token = StringField(required=False)


class Activity(Document):
    activity_id = StringField(required=False, default="A__" + getID())
    type = EnumField(required=True, enum=ActivityOptions)
    remark = GeoJsonBaseField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow())
