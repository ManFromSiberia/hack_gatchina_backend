from .settings import *

DEBUG = True
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
TELEGRAM_API_ID = 667537
TELEGRAM_API_HASH = '3173159e92cfd7f0b18ab8ec88f975c7'
