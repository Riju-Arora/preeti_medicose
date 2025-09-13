from pathlib import Path
import os
import dj_database_url  # only if you want Postgres later on Render

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Keep secret key hidden in production
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-key")

# ✅ For deployment set DEBUG=False
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ✅ Allowed hosts (local + Render domain)
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "preeti-medicose.onrender.com",  # replace with your actual Render domain
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',   # your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'preeti_medicose.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # ✅ point to templates folder
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

WSGI_APPLICATION = 'preeti_medicose.wsgi.application'

# ✅ Database (SQLite for dev, can switch to Postgres on Render)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# If Render provides DATABASE_URL (for Postgres), use it:
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Language, Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files config
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]   # your static folder
STATIC_ROOT = BASE_DIR / "staticfiles"     # where collectstatic puts everything
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
