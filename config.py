import settings

class SystemConfig:

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8'.format(**{
        'user': settings.DATABASE_USER,
        'password': settings.DATABASE_PASSWORD,
        'host': settings.DATABASE_HOST,
        'port': settings.DATABASE_PORT,
        'db_name': settings.DATABASE_NAME
    })

Config = SystemConfig