from dotenv import load_dotenv
import os
import dj_database_url
from pathlib import Path
from decouple import config

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PORT = int(os.environ.get('PORT', 8000))

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
INSTALLED_APPS = config('INSTALLED_APPS').split(',')
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')
MIDDLEWARE = config('MIDDLEWARE').split(',')

DEBUG = True

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

ROOT_URLCONF = 'zwojciechowic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zwojciechowic.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
WHITENOISE_USE_FINDERS = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LANGUAGES = [
    ('pl', 'Polski'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_IGNORE_MISSING_FILES = True


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
}





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

DEFAULT_CHARSET = 'utf-8'
EMAIL_CHARSET = 'utf-8'



os.makedirs(STATIC_ROOT, exist_ok=True)

if not DEBUG:
    if not isinstance(STATICFILES_DIRS, list):
        STATICFILES_DIRS = list(STATICFILES_DIRS)


ADMIN_SITE_HEADER = "🏡 Hodowla z Wojciechowic"
ADMIN_SITE_TITLE = "Hodowla Admin"
ADMIN_INDEX_TITLE = "Panel Zarządzania"

PARLER_LANGUAGES = {
    None: (
        {'code': 'pl',}, # Język domyślny
        {'code': 'en',},
    ),
    'default': {
        'fallback': 'pl',         # Język, na który wraca, gdy tłumaczenia brak
        'hide_untranslated': False, # Pokazuje wartość fallback, zamiast ukrywać obiekt
    }
}