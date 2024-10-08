import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''

    def __str__(self):
        return (
            f"Config:\n"
            f"  DEBUG: {self.DEBUG}\n"
            f"  SQLALCHEMY_DATABASE_URI : '{self.SQLALCHEMY_DATABASE_URI}'\n"
            f"  SECRET_KEY: '{self.SECRET_KEY}'\n"
        )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''


class DevelopmentSqliteConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///doc-server.db'
    SECRET_KEY = ''


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI ')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
