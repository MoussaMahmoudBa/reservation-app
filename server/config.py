import os
from decouple import config

# Django Settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Database
DB_NAME = config('DB_NAME', default='reservation_db')
DB_USER = config('DB_USER', default='postgres')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default='5432')

# Email Settings
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Cloudinary Settings
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default='')

# Redis Settings
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME = config('JWT_ACCESS_TOKEN_LIFETIME', default=1, cast=int)
JWT_REFRESH_TOKEN_LIFETIME = config('JWT_REFRESH_TOKEN_LIFETIME', default=7, cast=int) 

# Twilio SMS
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_FROM_NUMBER = config('TWILIO_FROM_NUMBER', default='')