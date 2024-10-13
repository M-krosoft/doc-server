import os


class _Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''
    GOOGLE_API_KEY = ''
    PORT = 5000

    def __str__(self):
        return (
            f"Config:\n"
            f"  DEBUG: {self.DEBUG}\n"
            f"  SQLALCHEMY_DATABASE_URI : '{self.SQLALCHEMY_DATABASE_URI}'\n"
            f"  SECRET_KEY: '{self.SECRET_KEY}'\n"
        )


class _DevelopmentConfig(_Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = ''


class _DevelopmentSqliteConfig(_Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///doc-server.db'
    SECRET_KEY = ''


class _ProductionConfig(_Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI ')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    PORT = os.environ.get('PORT')


class _TestingConfig(_Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def create_config(config_mode: str) -> _Config:
    if config_mode == 'dev':
        return _DevelopmentConfig()
    if config_mode == 'test':
        return _TestingConfig()
    if config_mode == 'prod':
        return _ProductionConfig()
    if config_mode == 'sqlite':
        return _DevelopmentSqliteConfig()
