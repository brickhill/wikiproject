from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY  = 'django-isdsdsfre-4u+9i52vhgt&3%+d)-#n2yi9@=xds-vhniiat@=zk+c(p$7jwx'

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
    'football'
]

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
        'DIRS': [],
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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = "static/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
