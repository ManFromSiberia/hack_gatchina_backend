from .settings import *

DEBUG = True
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
TELEGRAM_API_ID = ''
TELEGRAM_API_HASH = ''
TELEGRAM_BOT_TOKEN = ''
YANDEX_MAP_KEY = ''
MAPQUEST_MAP_KEY = ''
