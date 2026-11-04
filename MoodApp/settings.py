from pathlib import Path
import os
import dotenv
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read a local .env file if there is one (never commit it; see .env.example).
dotenv.load_dotenv(BASE_DIR / '.env')

# Debug is off unless DEBUG_FLAG=True is set (do that only on your own machine).
DEBUG = os.environ.get('DEBUG_FLAG', 'False') == 'True'

# The secret key comes from the environment. A throwaway key is used only for
# local development with DEBUG on; production refuses to start without one.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-development-only'
    else:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY is not set. Add it to the environment (Vercel: Settings > Environment Variables).'
        )

# Comma-separated host names. ".vercel.app" covers themoodapp.vercel.app and preview deployments.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '.vercel.app,localhost,127.0.0.1').split(',')
    if host.strip()
]

# The site is served over HTTPS on Vercel, so only send cookies over HTTPS there.
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'social',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'storages',  # Add django-storages
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

ROOT_URLCONF = 'MoodApp.urls'

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
                'django.template.context_processors.media',  # Add this to make MEDIA_URL available in templates
            ],
        },
    },
]

WSGI_APPLICATION = 'MoodApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Check if running on Vercel
IS_VERCEL = os.environ.get('VERCEL', False)

# Update to use Vercel Postgres or your preferred database
# Check if PostgreSQL environment variables are set
if os.environ.get('POSTGRES_DATABASE') and os.environ.get('POSTGRES_HOST'):
    # Use PostgreSQL if environment variables are available
    print("INFO: Using PostgreSQL database configuration")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DATABASE'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': '5432',
        }
    }
else:
    # Use SQLite as fallback for local development
    print("INFO: PostgreSQL environment variables not found. Using SQLite as fallback database")
    print(f"INFO: Database will be created at: {BASE_DIR / 'db.sqlite3'}")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Local media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = '/'
SITE_ID = 2
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET=True
ADMIN_SITE_HEADER = "Tazed Admin Block, Dont Even try udk the password, fuck u go away!!!!"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/' # REQUIRED SETTING
STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Ensure this is placed before the Media storage configuration block

# Media storage configuration
if not DEBUG:  # Use Vercel Blob in production
    DEFAULT_FILE_STORAGE = 'MoodApp.storage_backends.VercelBlobStorage'
    MEDIA_URL = 'https://3rm9kzfdjv9bixty.public.blob.vercel-storage.com/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# ... (rest of settings)
