from config.settings.common import *
from django.conf.global_settings import STATICFILES_FINDERS

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

SECRET_KEY = 'D[8mC)&*$HBN375,dPVVHwk_,xYH(q~UQV/*[:rIB@`DkG'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
