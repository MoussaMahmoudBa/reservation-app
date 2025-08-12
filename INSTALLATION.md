# 🏨 Guide d'Installation - Plateforme de Réservation Nouakchott

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** : [Télécharger Python](https://www.python.org/downloads/)
- **Node.js 16+** : [Télécharger Node.js](https://nodejs.org/)
- **Git** : [Télécharger Git](https://git-scm.com/)

## 🚀 Installation Rapide

### Option 1 : Script automatique (Recommandé)

```bash
# Rendre le script exécutable
chmod +x start.sh

# Démarrer l'application
./start.sh
```

### Option 2 : Installation manuelle

#### 1. Backend Django

```bash
# Aller dans le dossier server
cd server

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

#### 2. Frontend React

```bash
# Aller dans le dossier client
cd client

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `server/` :

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optionnel pour le développement)
DB_NAME=reservation_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary Settings (optionnel)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Redis Settings (optionnel)
REDIS_URL=redis://localhost:6379/0
```

### Base de données

Par défaut, l'application utilise SQLite pour le développement. Pour utiliser PostgreSQL :

1. Installez PostgreSQL
2. Créez une base de données
3. Configurez les variables d'environnement
4. Décommentez la configuration PostgreSQL dans `settings.py`

## 🌐 Accès à l'application

Une fois démarrée, l'application sera accessible sur :

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin

### Comptes par défaut

- **Superutilisateur** : admin / admin123
- **Utilisateur test** : user / password123

## 📁 Structure du projet

```
Reservation/
├── server/                 # Backend Django
│   ├── reservation_project/ # Configuration Django
│   ├── users/             # Gestion des utilisateurs
│   ├── hotels/            # Gestion des hôtels
│   ├── apartments/        # Gestion des appartements
│   ├── reservations/      # Gestion des réservations
│   └── requirements.txt   # Dépendances Python
├── client/                # Frontend React
│   ├── src/
│   │   ├── components/    # Composants React
│   │   ├── pages/         # Pages de l'application
│   │   ├── services/      # Services API
│   │   └── types/         # Types TypeScript
│   └── package.json       # Dépendances Node.js
├── docs/                  # Documentation
├── start.sh              # Script de démarrage
└── README.md             # Documentation principale
```

## 🛠️ Développement

### Backend

```bash
cd server
source venv/bin/activate

# Créer une nouvelle migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer les tests
python manage.py test

# Démarrer le serveur
python manage.py runserver
```

### Frontend

```bash
cd client

# Installer de nouvelles dépendances
npm install package-name

# Lancer les tests
npm test

# Build pour la production
npm run build

# Démarrer le serveur de développement
npm start
```

## 🔍 Débogage

### Problèmes courants

1. **Erreur de migration** : Supprimez le fichier `db.sqlite3` et relancez les migrations
2. **Erreur de port** : Changez le port dans `settings.py` ou `package.json`
3. **Erreur de dépendances** : Supprimez `node_modules` et `venv`, puis réinstallez

### Logs

- **Django** : Les logs apparaissent dans la console
- **React** : Les logs apparaissent dans la console du navigateur

## 🚀 Déploiement

### Production

1. Configurez une base de données PostgreSQL
2. Configurez les variables d'environnement
3. Build du frontend : `npm run build`
4. Collectez les fichiers statiques : `python manage.py collectstatic`
5. Configurez un serveur web (Nginx + Gunicorn)

### Docker (optionnel)

```bash
# Build des images
docker-compose build

# Démarrer les services
docker-compose up -d
```

## 📞 Support

Pour toute question ou problème :

1. Consultez la documentation
2. Vérifiez les logs
3. Créez une issue sur GitHub
4. Contactez l'équipe de développement

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 