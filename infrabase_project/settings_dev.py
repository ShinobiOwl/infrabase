from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Override MySQL with SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}