import os

class Config():
    SECRET_KEY = '%yt1uvp5-v52s=+(kt)fan$nne$b4s5u(+*o)b(0cd_)hkzp30'

    DB_USER = "app"
    DB_HOST = 'db'
    DB_PASS = 'pass'

    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DB_USER = "app"
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pw}@{host}/{db}'.format(
        user=DB_USER, pw=DB_PASS, host=DB_HOST, db=DB_NAME)

class TestingConfig(Config):
    DB_USER = "app"
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pw}@{host}/{db}'.format(
        user=DB_USER, pw=DB_PASS, host=DB_HOST, db=DB_NAME)

class ProductionConfig(Config):
    DB_USER = "app"
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Production'
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pw}@{host}/{db}'.format(
        user=DB_USER, pw=DB_PASS, host=DB_HOST, db=DB_NAME)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
