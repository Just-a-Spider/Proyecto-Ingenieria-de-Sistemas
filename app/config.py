import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='your_secret_key')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='mysql://username:password@localhost/db_name')
    SQLALCHEMY_TRACK_MODIFICATIONS = False