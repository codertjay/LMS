import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy
import vimeo
from newsapi import NewsApiClient


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["*", ]
else:
    ALLOWED_HOSTS = [".assassinfx.com", ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

]

LocalInstalledApps = [
    'users',
    'courses',
    'memberships',
    'blog',
    'home_page',
    'academy_forum',
    'signal_app',
    'copy_trading',
    '_coupon',
    'extensions',
    'academy_dashboard',
]

ExternalInstalledApps = [
    'upload_validator',
    'pagedown',
    'import_export',
    'crispy_forms',
    # django hosts
    'django_hosts',

    'allauth',
    'allauth.account',
    #  social account
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_cleanup.apps.CleanupConfig',
]

INSTALLED_APPS += ExternalInstalledApps
INSTALLED_APPS += LocalInstalledApps

MIDDLEWARE = [
    # for django host
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # for django host
    'django_hosts.middleware.HostsResponseMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.add_variable_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Learning_platform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('POSTGRESDB_NAME', default=''),
            'USER': config('POSTGRESDB_USER', default=''),
            'PASSWORD': config('POSTGRESDB_PASSWORD', default=''),
            'HOST': config('POSTGRESDB_HOST', default=''),
            'PORT': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_root'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'courses/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if DEBUG:
    LOGIN_URL = "http://www.assassinfx.com/accounts/login/"
else:
    LOGIN_URL = "http://www.assassinfx.com/accounts/login/"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SIGNUP_REDIRECT_URL = '/courses/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_UNIQUE_USERNAME = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 200
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = []

if DEBUG:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51I7JYzAS6n0shLOqDkhsxVyZT7OjVlrft7uQy8trLzmKf6OoYVFuUrjtJwUvXJcq00MYTcARgbaTHK5XiKUm7ig400bTTOaknZ'
    STRIPE_SECRET_KEY = 'sk_test_51I7JYzAS6n0shLOq6XZJdgF0ihJh4ZanPMqWMELlomYfJ3vZXQwq4kWj4fsXhsOsWE1DQm0AgIV2pD7yZcKEyKG9005LDdWKEU'
else:
    # live keys
    STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
    STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')

# Django allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# for sending email
if DEBUG:
    EMAIL_HOST_USER_SENDGRID = 'begintjay@gmail.com'
else:
    EMAIL_HOST_USER_SENDGRID = 'ninjaassassin@assassinfx.com'

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

SENDGRID_API_KEY = config('SENDGRID_API_KEY')

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER_SENDGRID

#  handling errors for demo
handler404 = 'home_page.views.view_404'
handler500 = 'home_page.views.view_500'
handler403 = 'home_page.views.view_403'
handler400 = 'home_page.views.view_400'



# django host
DEFAULT_HOST = 'www'
ROOT_HOSTCONF = 'Learning_platform.hosts'
ROOT_URLCONF = 'Learning_platform.urls'

DOMAIN_NAME = 'assassinfx.com'
if DEBUG:
    PARENT_HOST = f'{DOMAIN_NAME}:8000'
    DEFAULT_REDIRECT_URL = f"http://{DOMAIN_NAME}:8000"
else:
    PARENT_HOST = DOMAIN_NAME
    DEFAULT_REDIRECT_URL = f"https://{DOMAIN_NAME}"

CSRF_TRUSTED_ORIGINS = [f"{'.' + DOMAIN_NAME}", f"academy.{DOMAIN_NAME}", f"www.{DOMAIN_NAME}",
                        'academy.assassinfx.com']
SESSION_COOKIE_DOMAIN = f".{DOMAIN_NAME}"

SESSION_COOKIE_NAME = 'assassinfxsessionid'

CSRF_COOKIE_DOMAIN = '.' + DOMAIN_NAME

# CSRF_USE_SESSIONS = True

VIMEO_AUTHENTICATE = vimeo.VimeoClient(
    token="4065ff3ed3daf6307a7b09ba9076e841",
    key="19c6d96a4a45af44348ef9516002f11f93ec0290",
    secret="brfCb290lRxOGM0fFAHu1NATjxiDsClBHEVd6Sa1l8Sa1Jpm4PEDmCkC+51T5dRkJtXVT6efhDVp894ZMTUqcgQ5XBYtLxHZHPzNl4+LmFuYFkmk8ThPXzkOucAqXlFN"
)
newsapi = NewsApiClient(api_key= config('NewApiKey', default=''))



# top_headlines = newsapi.get_top_headlines(q='bitcoin', sources='bbc-news,the-verge',category='business', language='en')
