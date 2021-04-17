import os

# flask
DEBUG = False
USER = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOSTNAME')
DB = os.environ.get('DB_NAME')

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask_sample?charset=utf8'.format(**{
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'db': DB
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
