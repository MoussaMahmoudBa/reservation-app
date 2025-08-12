Configuration des données réelles et Cloudinary

1) Variables d'environnement (.env à la racine de `server/`)

Exemple:

SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de données
DB_ENGINE=postgres
DB_NAME=reservation_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

2) Installer les dépendances et initialiser la DB

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

3) Créer un superuser

python manage.py createsuperuser

4) Lancer le serveur

python manage.py runserver 0.0.0.0:8000

5) Seeder (données de base)

python manage.py seed_demo_data --hotels --apartments --users

