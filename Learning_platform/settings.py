import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', '.localhost', 'localhost', '104.248.230.206','assassinfx.com','www.assassinfx.com']
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'users',
    'courses',
    'memberships',
    'blog',
    'home_page',
    'forum',
    'signal_app',
    'copy_trading',

    'upload_validator',
    'pagedown',
    'import_export',
    'crispy_forms',

    'allauth',
    'allauth.account',
    #  social account
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'django_cleanup.apps.CleanupConfig',
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

ROOT_URLCONF = 'Learning_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/courses/'
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='')
#  handling errors for demo
handler404 = 'home_page.views.view_404'
handler500 = 'home_page.views.view_500'
handler403 = 'home_page.views.view_403'
handler400 = 'home_page.views.view_400'
ADMINS = (
    ('codertjay', 'begintjay@email.com'),
)
MANAGERS = ADMINS
SITE_URL = "https://assassinfx.com/"
