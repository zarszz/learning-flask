import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://postgres:password@127.0.0.1:5432/learn_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
