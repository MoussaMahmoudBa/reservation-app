# Configuration par défaut pour le développement
# Copiez ce fichier vers .env et modifiez les valeurs selon vos besoins

# Django Settings
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'
DEBUG = True
ALLOWED_HOSTS = 'localhost,127.0.0.1'

# Database
DB_NAME = 'reservation_db'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'

# Email Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Cloudinary Settings
CLOUDINARY_CLOUD_NAME = 'your-cloud-name'
CLOUDINARY_API_KEY = 'your-api-key'
CLOUDINARY_API_SECRET = 'your-api-secret'

# Redis Settings
REDIS_URL = 'redis://localhost:6379/0'

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME = 1
JWT_REFRESH_TOKEN_LIFETIME = 7 

# Twilio SMS
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_FROM_NUMBER = ''