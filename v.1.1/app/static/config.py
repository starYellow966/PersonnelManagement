import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i do not how to use it'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    
    # @staticmethod
    # def init_app(app):
    #     app.config['SECRET_KEY'] = SECRET_KEY
    #     app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = SQLALCHEMY_COMMIT_ON_TEARDOWN
    #     return app


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://hx:huangxin123456@localhost/gdesignV1_1?charset=utf8'
    UPLOADED_PHOTOS_DEST = './photos'
    """docstring for DevelopmentConfig"""
    def __init__(self, arg):
        super(DevelopmentConfig, self).__init__()
        self.arg = arg
    
    # @staticmethod
    # def init_app(app):
    #     super(app)
    #     config['']
        

class TestingConfig(Config):
    TESTING = True
    UPLOADED_PHOTOS_DEST = 'E://photos'
    SQLALCHEMY_DATABASE_URI = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8'

class ProductionConfig(Config):
    UPLOADED_PHOTOS_DEST = 'E://photos'
    SQLALCHEMY_DATABASE_URI = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
