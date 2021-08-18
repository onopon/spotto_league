from instance import settings

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(**{
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'host': settings.DB_HOST,
    'db': settings.DB_NAME
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# AttributeError: 'Request' object has no attribute 'is_xhr' 対策
JSONIFY_PRETTYPRINT_REGULAR = False
