import os

class Config():
    SECRET_KEY = '%yt1uvp5-v52s=+(kt)fan$nne$b4s5u(+*o)b(0cd_)hkzp30';
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
