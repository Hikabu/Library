import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-k1!svx5pna71t3&y#w!9iie&5p2)7)0acb9%@k788a@2y=9r54"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['*']

#Does this backend recognize this user and their credentials?
#modelbackend - checks the database for a user with the provided username and password.
#intra - Validating users based on an oauth, API
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'project.apps.intrauth.auth.IntraAuthenticationBackend'
]
# so django will not use will use the default User model - easier migrations- just add new fields
AUTH_USER_MODEL = 'intrauth.CustomUser'

# Application definition

INSTALLED_APPS = [
    # Built-in Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-Party Apps
    "corsheaders",
    "channels",
    "rest_framework",
    "rest_framework_simplejwt",
    "django.contrib.postgres",
    "rest_framework_simplejwt.token_blacklist",
    # Custom Project Apps
    "project.apps.pong",
    "project.apps.custom_auth",
    "project.apps.intrauth",
    "storages",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',#compresses and caches static files, reducing load times.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = "project.urls"

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
            ],
        },
    },
]

ASGI_APPLICATION = "project.asgi.application"
WSGI_APPLICATION = "project.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

#AWS configs
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_SIGNATURE_NAME = 's3v4'

# AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

#this one is for media files, you can keep it if you're using media
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"

MEDIAFILES_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"

STORAGES = {
    "default": {"BACKEND": "project.storage.MediaStorage"},
    "staticfiles": {"BACKEND": "project.storage.StaticStorage"},
}
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=2592000", # 2 days 
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOW_CREDENTIALS = True #?
CSRF_COOKIES_HTTPONLY = False # Allows JS to read the CSRF cookie
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False 

# Allow WebSocket connections
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "https://localhost",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
    "http://django-transendence.s3-website-us-east-1.amazonaws.com",
]


"""
    rest - how the framework handles authentication and permissions for API endpoints
        The server validates the token to authenticate the user and 
    ensures that only authenticated users can access the API endpoints.

REST_FRAMEWORK = {
    'STATIC_URL': STATIC_URL,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'project.apps.custom_auth.authentication.CookieJwtAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # For unauthenticated users
    },
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=11), #how long tokens are valid
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    
    # JWT creation and validation.
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    
    # Authentication Header
    'AUTH_HEADER_TYPES': ('Bearer',), #token must be sent in the Authorization header with the prefix Bearer
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    #ti strict security set ti true was in dock 
    'ROTATE_REFRESH_TOKENS': True,#a new refresh token is issued every time an access token is refreshed.!!!will change with the access token
    'BLACKLIST_AFTER_ROTATION': True,#old refresh tokens are blacklisted after rotation to prevent reuse.
    
    #tracking user activity not useful 
    'UPDATE_LAST_LOGIN': True,
    
    #for frontend if store in cookies very important for local just delete 
    'AUTH_COOKIE_ACCESS': 'access_token',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
    'AUTH_COOKIE_HTTP_ONLY': True,# Prevents JavaScript from accessing the cookie
    'AUTH_COOKIE_SECURE': True,#Ensures the cookie is only sent over HTTPS.
    'AUTH_COOKIE_SAMESITE': 'Lax',#Controls cross-site request if the post request the cookies will be not sented(lax)
    #User Identification
    'USER_ID_FIELD': 'id', #tells the server which field in the database identifies the user
    'USER_ID_CLAIM': 'user_id',#where to find the user"s id in the jwt blabla
    
    "JTI_CLAIM": "jti",
    
    #Token Classes
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "channels": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        'level': 'DEBUG'
    },
}
