# 🏨 Application de Réservation d'Hôtels et Appartements

Une application web moderne pour la réservation d'hôtels et d'appartements, construite avec Django REST Framework et React.

## 🚀 Déploiement

### Option 1 : Railway (Recommandé)

1. **Préparer le repository**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Créer un compte Railway**
   - Allez sur [railway.app](https://railway.app)
   - Créez un compte avec GitHub

3. **Déployer le backend Django**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository
   - Railway détectera automatiquement Django

4. **Configurer les variables d'environnement**
   ```
   SECRET_KEY=votre-secret-key-securise
   DEBUG=False
   DB_ENGINE=postgres
   DB_NAME=railway
   DB_USER=postgres
   DB_PASSWORD=railway
   DB_HOST=containers-us-west-XX.railway.app
   DB_PORT=5432
   CLOUDINARY_CLOUD_NAME=dcbnzgymz
   CLOUDINARY_API_KEY=votre-api-key
   CLOUDINARY_API_SECRET=votre-api-secret
   ```

5. **Déployer le frontend React**
   - Créez un nouveau service dans le même projet
   - Sélectionnez "Static Site"
   - Configurez le dossier `client/build`

### Option 2 : Render

1. **Backend Django**
   - Créez un compte sur [render.com](https://render.com)
   - Créez un nouveau "Web Service"
   - Connectez votre repository GitHub
   - Configurez :
     - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - Start Command: `gunicorn reservation_project.wsgi:application`

2. **Frontend React**
   - Créez un nouveau "Static Site"
   - Configurez le dossier `client/build`

## 🔧 Configuration Locale

### Backend Django
```bash
cd server
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend React
```bash
cd client
npm install
npm start
```

## 📁 Structure du Projet

```
Reservation/
├── server/                 # Backend Django
│   ├── reservation_project/
│   ├── users/
│   ├── hotels/
│   ├── apartments/
│   └── reservations/
├── client/                 # Frontend React
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt        # Dépendances Python
├── Procfile               # Configuration Railway
└── README.md
```

## 🌐 Variables d'Environnement

### Backend (.env)
```
SECRET_KEY=votre-secret-key
DEBUG=True
DB_ENGINE=postgres
DB_NAME=reservation_db
DB_USER=postgres
DB_PASSWORD=Moussa123
DB_HOST=localhost
DB_PORT=5433
CLOUDINARY_CLOUD_NAME=dcbnzgymz
CLOUDINARY_API_KEY=votre-api-key
CLOUDINARY_API_SECRET=votre-api-secret
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_CLOUDINARY_CLOUD_NAME=dcbnzgymz
REACT_APP_CLOUDINARY_UPLOAD_PRESET=reservation
```

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.0, Django REST Framework, PostgreSQL
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Stockage**: Cloudinary
- **Déploiement**: Railway/Render

## 📞 Support

Pour toute question ou problème, contactez l'équipe de développement. 