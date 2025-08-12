"""
Django settings for production deployment.
"""

import os
from pathlib import Path
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration de production
DEBUG = False

# Autoriser tous les hôtes pour le moment (à configurer plus tard)
ALLOWED_HOSTS = ['*']

# Configuration CORS pour permettre l'accès depuis Vercel
CORS_ALLOWED_ORIGINS = [
    "https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app",
    "https://vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Autoriser les credentials
CORS_ALLOW_CREDENTIALS = True

# Configuration de la base de données PostgreSQL pour Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'railway'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration de sécurité
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configuration des sessions
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configuration des logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
} 