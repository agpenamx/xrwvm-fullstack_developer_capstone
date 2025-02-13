import os
from pathlib import Path
from dotenv import load_dotenv  # ✅ Load environment variables

# ✅ Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Improved Security for Secret Key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-ccow$tz_=9%dxu4(0%^(z%nx32#s@(zt9$ih@)5l54yny)wm-0")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# ✅ Merged ALLOWED_HOSTS from both versions
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.proxy.cognitiveclass.ai',  # IBM Cloud proxy
    os.getenv('backend_url', '').split('//')[-1]
]

# ✅ Merged CSRF_TRUSTED_ORIGINS with Validation
CSRF_TRUSTED_ORIGINS = [
    'https://agpenamx-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai',
    os.getenv('backend_url', 'https://default.proxy.cognitiveclass.ai')
]
if not CSRF_TRUSTED_ORIGINS[-1].startswith(('http://', 'https://')):
    CSRF_TRUSTED_ORIGINS[-1] = f"https://{CSRF_TRUSTED_ORIGINS[-1]}"

# ✅ Installed Applications (Merged from both versions)
INSTALLED_APPS = [
    'djangoapp.apps.DjangoappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ✅ Merged Middleware (Added WhiteNoise for Static Files)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Static file optimization
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoproj.urls'

# ✅ Merged Template Directories (Ensured React Build is Included)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend/static'),
            os.path.join(BASE_DIR, 'frontend/build'),
            os.path.join(BASE_DIR, 'frontend/build/static'),
        ],
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

WSGI_APPLICATION = 'djangoproj.wsgi.application'

# ✅ Merged Database Configuration (Keeping MongoDB Support)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongo': {
        'ENGINE': 'djongo',
        'NAME': os.getenv('MONGO_DB_NAME', 'dealershipDB'),
        'HOST': os.getenv('MONGO_DB_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('MONGO_DB_PORT', 27017)),
        'USER': os.getenv('MONGO_DB_USER', ''),
        'PASSWORD': os.getenv('MONGO_DB_PASSWORD', ''),
        'AUTH_SOURCE': os.getenv('MONGO_DB_AUTH_SOURCE', 'admin'),
    }
}

# ✅ Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ✅ Merged Static and Media Files Handling (Added WhiteNoise Storage)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/static'),
    os.path.join(BASE_DIR, 'frontend/build'),
    os.path.join(BASE_DIR, 'frontend/build/static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
