"""
Module that contains all flask config settings for the flask app
"""
import os
from datetime import timedelta

DEBUG = True

# """Set to be able to run pytest natively in docker"""
SERVER_NAME = 'localhost:8000'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Flask-Mail
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

# REDIS Configuration
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'devpassword')

# Celery Configuration
CELERY_BROKER_URL = f"redis://:{os.environ.get('REDIS_PASSWORD')}@redis:6379/0"
CELERY_RESULT_BACKEND = f"redis://:{os.environ.get('REDIS_PASSWORD')}@redis:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)
