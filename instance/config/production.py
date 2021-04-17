import os

# flask
DEBUG = False
USER = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOSTNAME')
DB = os.environ.get('DB_NAME')

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/flask_sample?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', USER),
    'password': os.getenv('DB_PASSWORD', PASSWORD),  # あとで変える（何に変えるのが適切なんだろ）
    'host': os.getenv('DB_HOST', HOST),
    'db': DB
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
