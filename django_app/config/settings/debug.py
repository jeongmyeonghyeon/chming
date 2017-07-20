# debug.py
from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

# WSGI application
WSGI_APPLICATION = 'config.wsgi.debug.application'

INSTALLED_APPS.append('django_extensions')

# Static URLs
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# 디버그모드니까 DEBUG는 False
DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)
