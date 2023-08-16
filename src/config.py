from dynaconf import Dynaconf

ALLOWED_EXTENSIONS = ('jpg', 'png', 'jpeg')

settings = Dynaconf(settings_files=['settings.toml'], environment=True)

def get_rabbit_config():
    if settings.APP_SETTINGS == 'testing':
        return 'memory://'
    return ("amqp://"
            f"{settings.BROKER_USER}:{settings.BROKER_PASSWORD}@"
            f"{settings.BROKER_HOST}:{settings.BROKER_PORT}/"
            f"{settings.BROKER_VHOST}")

def get_db_config():
    if settings.APP_SETTINGS == 'testing':
        return "sqlite:///database.db"
    return ("postgresql://"
            f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
            f"{settings.POSTGRES_DB}")