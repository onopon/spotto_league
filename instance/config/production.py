import os

# flask
DEBUG = False
USER = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOSTNAME')
DB = os.environ.get('DB_NAME')
USER = "spotto"
PASSWORD = "ExZ4qV2kucNWYcJSR3CuZHRQ5QrYMR92"
HOST = "153.121.51.117"
DB = "spotto"

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'db': DB
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
