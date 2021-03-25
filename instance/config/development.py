import os

# flask
DEBUG = True

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'db': 'spotto_dev'
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
