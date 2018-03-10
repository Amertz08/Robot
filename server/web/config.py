import os

try:
    from local_config import SMTP
except ImportError:
    print("""
    local_config.py not setup properly
    V example V

    SMTP = {
        'user': '', # Gmail account
        'pw': '' # Gmail password
    }
    """)
    exit(1)


class Config(object):
    SECRET_KEY = '%yt1uvp5-v52s=+(kt)fan$nne$b4s5u(+*o)b(0cd_)hkzp30'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = SMTP['user']
    MAIL_PASSWORD = SMTP['pw']

    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DB_USER = 'app'
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

class TestingConfig(Config):
    DB_USER = 'app'
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

class ProductionConfig(Config):
    DB_USER = 'app'
    DB_HOST = 'db'
    DB_PASS = 'pass'
    DB_NAME = 'Production'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
