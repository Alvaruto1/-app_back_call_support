class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = 'secret-key-goes-here'
    CORS_HEADERS = 'Content-Type'
    JWTSECRETKEY = 'secret-key-jwt'
    JWT_ALGORITHM = 'HS256'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

 