# 🚀 Guide de Déploiement - Application de Réservation

## 📋 Prérequis

- Compte GitHub
- Compte Railway (gratuit) ou Render (gratuit)
- Compte Cloudinary (gratuit)

## 🔧 Étape 1 : Créer un Repository GitHub

1. **Allez sur GitHub.com** et créez un nouveau repository
2. **Nommez-le** : `reservation-app` ou `hotel-booking`
3. **Ne pas initialiser** avec README (nous avons déjà le code)

## 🔗 Étape 2 : Connecter le Repository Local

```bash
# Dans votre dossier de projet
git remote add origin https://github.com/VOTRE_USERNAME/reservation-app.git
git push -u origin main
```

## 🚂 Étape 3 : Déployer sur Railway

### 3.1 Créer un compte Railway
1. Allez sur [railway.app](https://railway.app)
2. Connectez-vous avec GitHub
3. Cliquez sur "New Project"

### 3.2 Déployer le Backend Django
1. **Sélectionnez** "Deploy from GitHub repo"
2. **Choisissez** votre repository
3. **Railway détectera** automatiquement Django
4. **Attendez** le déploiement initial

### 3.3 Configurer les Variables d'Environnement
Dans Railway, allez dans "Variables" et ajoutez :

```env
SECRET_KEY=votre-secret-key-tres-securise-ici
DEBUG=False
DB_ENGINE=postgres
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=railway
DB_HOST=containers-us-west-XX.railway.app
DB_PORT=5432
CLOUDINARY_CLOUD_NAME=dcbnzgymz
CLOUDINARY_API_KEY=votre-cloudinary-api-key
CLOUDINARY_API_SECRET=votre-cloudinary-api-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password
```

### 3.4 Configurer la Base de Données
1. Dans Railway, allez dans "Resources"
2. Cliquez sur "New"
3. Sélectionnez "Database" → "PostgreSQL"
4. Railway créera automatiquement les variables DB_*

### 3.5 Exécuter les Migrations
1. Dans Railway, allez dans "Deployments"
2. Cliquez sur "Deploy Now"
3. Les migrations s'exécuteront automatiquement

### 3.6 Créer un Superuser
Dans Railway, allez dans "Deployments" → "View Logs" et exécutez :
```bash
python manage.py createsuperuser
```

## 🌐 Étape 4 : Déployer le Frontend React

### 4.1 Build du Frontend
```bash
cd client
npm run build
cd ..
```

### 4.2 Créer un Service Frontend sur Railway
1. Dans votre projet Railway, cliquez sur "New"
2. Sélectionnez "Static Site"
3. Configurez :
   - **Source Directory**: `client/build`
   - **Build Command**: `cd client && npm install && npm run build`
   - **Output Directory**: `build`

### 4.3 Configurer les Variables Frontend
Dans le service frontend, ajoutez :
```env
REACT_APP_API_URL=https://votre-backend-railway-url.railway.app/api
REACT_APP_CLOUDINARY_CLOUD_NAME=dcbnzgymz
REACT_APP_CLOUDINARY_UPLOAD_PRESET=reservation
```

## 🔧 Étape 5 : Configuration Cloudinary

1. **Allez sur Cloudinary.com** et créez un compte
2. **Notez** vos credentials :
   - Cloud Name
   - API Key
   - API Secret
3. **Créez un Upload Preset** :
   - Dashboard → Settings → Upload
   - Scroll down → Upload presets
   - Create upload preset
   - Nommez-le "reservation"
   - Signing Mode: "Unsigned"

## 🔗 Étape 6 : Domaines Personnalisés (Optionnel)

### Backend
1. Dans Railway, allez dans "Settings"
2. "Custom Domains"
3. Ajoutez votre domaine (ex: api.votresite.com)

### Frontend
1. Dans le service frontend, "Settings"
2. "Custom Domains"
3. Ajoutez votre domaine (ex: votresite.com)

## 🧪 Étape 7 : Test du Déploiement

### Test Backend
```bash
curl https://votre-backend-url.railway.app/api/hotels/
```

### Test Frontend
1. Visitez votre URL frontend
2. Testez la connexion
3. Testez l'ajout d'un hôtel
4. Testez une réservation

## 🔒 Étape 8 : Sécurité

### Variables Sensibles
- ✅ SECRET_KEY : Utilisez un générateur de clé sécurisé
- ✅ CLOUDINARY_* : Gardez vos credentials privés
- ✅ EMAIL_* : Utilisez un mot de passe d'application Gmail

### HTTPS
- Railway fournit automatiquement HTTPS
- Pas de configuration supplémentaire nécessaire

## 📊 Étape 9 : Monitoring

### Logs
- Railway → Deployments → View Logs
- Surveillez les erreurs 500
- Vérifiez les performances

### Métriques
- Railway → Metrics
- Surveillez l'utilisation CPU/Mémoire
- Surveillez les requêtes

## 🚨 Dépannage

### Erreur 500
1. Vérifiez les logs Railway
2. Vérifiez les variables d'environnement
3. Vérifiez la base de données

### Erreur CORS
1. Vérifiez CORS_ALLOWED_ORIGINS
2. Ajoutez votre domaine frontend

### Erreur Database
1. Vérifiez les variables DB_*
2. Exécutez les migrations
3. Vérifiez la connexion

## 📞 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)
- **React Docs**: [reactjs.org](https://reactjs.org)

## 🎉 Félicitations !

Votre application est maintenant déployée et accessible en ligne ! 