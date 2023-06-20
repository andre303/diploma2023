"""
Django settings for ubetrip project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku
import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."
# PRODUCTION:
# Heroku -> Config Vars -> SECRET_KEY 
# https://dashboard.heroku.com/apps/ubetrip/settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# PRODUCTION:
# Heroku -> Config Vars -> DEBUG
# https://dashboard.heroku.com/apps/ubetrip/settings

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",
    "trips",
    "rosetta",
    'social_django',
    'crispy_forms',
    'import_export',
    'cloudinary',
    # 'uni_form',
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'trips.middleware.SettingsMiddleware',
]

ROOT_URLCONF = "ubetrip.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "ubetrip.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# ВАЖЛИВІ ДАНІ
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ubertrip',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#GOOGLE
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

#FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = ''        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = ''  # App Secret

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'travelfindo',
    'API_KEY': '',
    'API_SECRET': '',
}
cloudinary.config(
    cloud_name = 'travelfindo', 
    api_key = '',
    api_secret =''
)

#EMAIL HOST

EMAIL_HOST_USER = 'travelfindotest1@gmail.com'
EMAIL_HOST_PASSWORD = 'bgguworuaqeyztsj'



EMAIL_BACKEND =  'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ('en', 'English'),
    ('uk', 'Ukrainian'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

django_heroku.settings(locals())

# PRODUCTION:
if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

#AUTH
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    
)

# TEST
# SOCIAL_AUTH_FACEBOOK_KEY = '1460117587661111'        # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = 'c28edadc9031ba421c9ded9fe7455340'  # App Secret


SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]
SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {
    'auth_type': ''
}


SOCIAL_AUTH_PIPELINE = (
   'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email', 
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # 'social.pipeline.social_auth.associate_user',

)

LOGIN_URL = '/auth/login/google-oauth2/'

LOGIN_REDIRECT_URL = 'social_login'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# Crispy
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#CONTEXT PROCESSOR
TEMPLATES[0]['OPTIONS']['context_processors'].append("trips.context_processors.register_processor")
TEMPLATES[0]['OPTIONS']['context_processors'].append("trips.context_processors.isGuide_processor")

