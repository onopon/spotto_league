import os

# flask
DEBUG = True
ROOT = 'root'
PASSWORD = ''
HOST = 'localhost'
DB = 'spotto_dev'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', ROOT),
    'password': os.getenv('DB_PASSWORD', PASSWORD),
    'host': os.getenv('DB_HOST', HOST),
    'db': DB
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
