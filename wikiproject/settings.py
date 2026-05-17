from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
# TODO How do I automatically resize images on upload?
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-sfre-4u+9i52vhgt&3%+d)-#n2yi9@=xds-vhniiat@=zk+c(p$7jwx'

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "whitchurch.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'football',
    'blog',
    'crispy_forms',
    'crispy_bootstrap5',
    'cookie_consent'
]
# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Ckeditor
INSTALLED_APPS += ['ckeditor', 'ckeditor_uploader']
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join([
            'codesnippet',
        ]),
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wikiproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # App level templates.
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

WSGI_APPLICATION = 'wikiproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'production': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Whitchurch$wikidata',
        'USER': 'Whitchurch',
        'PASSWORD': 'PumPyTr0u53r5!',
        'HOST': 'Whitchurch.mysql.pythonanywhere-services.com',
    }
}

try:
    file = open("dev.txt", "r")
    DEBUG = True
    contents = file.read()
    print('DEV Environment')
    print(f"CONTENTS: {contents}")  # Print file content

except Exception as e:
    DEBUG = False
    print(f"LIVE Environment:{e}")
    DATABASES['default'] = DATABASES['production']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
print(f"RESEND_API:{RESEND_API_KEY}")
