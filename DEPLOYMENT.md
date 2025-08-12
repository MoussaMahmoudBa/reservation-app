# Guide de Déploiement - Application de Réservation

Ce guide vous explique comment déployer l'application de réservation sur Netlify (Frontend) et Render.com (Backend).

## 🏗️ Architecture de Déploiement

- **Frontend (React.js)**: Netlify
- **Backend (Django)**: Render.com
- **Base de données**: PostgreSQL sur Render.com
- **Stockage de fichiers**: Cloudinary

## 🚀 1. Déploiement Backend sur Render.com

### Étape 1: Créer un compte Render.com
1. Allez sur [render.com](https://render.com)
2. Créez un compte ou connectez-vous

### Étape 2: Créer la base de données PostgreSQL
1. Dans le dashboard Render, cliquez sur "New +"
2. Sélectionnez "PostgreSQL"
3. Configurez :
   - **Name**: `reservation-postgres`
   - **Database**: `reservation_db`
   - **User**: `reservation_user`
   - **Plan**: Free
4. Cliquez sur "Create Database"
5. Notez l'URL de connexion (DATABASE_URL)

### Étape 3: Déployer le service Django
1. Dans le dashboard Render, cliquez sur "New +"
2. Sélectionnez "Web Service"
3. Connectez votre repository GitHub
4. Configurez :
   - **Name**: `reservation-backend`
   - **Root Directory**: `server`
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn reservation_project.wsgi:application`
   - **Plan**: Free

### Étape 4: Configurer les variables d'environnement
Dans les paramètres du service, ajoutez ces variables :

```
SECRET_KEY=your-secret-key-here
DEBUG=false
DATABASE_URL=postgres://... (from your PostgreSQL service)
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Étape 5: Déployer
1. Cliquez sur "Create Web Service"
2. Render va automatiquement déployer votre application
3. Notez l'URL de votre service (ex: `https://reservation-backend.onrender.com`)

## 🌐 2. Déploiement Frontend sur Netlify

### Étape 1: Créer un compte Netlify
1. Allez sur [netlify.com](https://netlify.com)
2. Créez un compte ou connectez-vous

### Étape 2: Connecter le repository
1. Cliquez sur "New site from Git"
2. Connectez votre repository GitHub
3. Configurez :
   - **Base directory**: `client`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

### Étape 3: Configurer les variables d'environnement
Dans les paramètres du site, ajoutez :

```
REACT_APP_API_URL=https://your-backend-url.onrender.com/api
```

### Étape 4: Déployer
1. Cliquez sur "Deploy site"
2. Netlify va automatiquement déployer votre application
3. Notez l'URL de votre site (ex: `https://your-app-name.netlify.app`)

## 🔧 3. Configuration CORS

### Mettre à jour les domaines autorisés
Dans `server/reservation_project/settings.py`, mettez à jour :

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Production domains
    "https://your-app-name.netlify.app",
    "https://your-backend-url.onrender.com",
]
```

## 📧 4. Configuration Email (Optionnel)

Pour activer l'envoi d'emails, configurez dans Render.com :

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🖼️ 5. Configuration Cloudinary (Optionnel)

Pour le stockage d'images, créez un compte Cloudinary et configurez :

```
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## 🔄 6. Déploiement automatique

### Render.com
- Le déploiement est automatique à chaque push sur la branche principale
- Les migrations de base de données s'exécutent automatiquement

### Netlify
- Le déploiement est automatique à chaque push sur la branche principale
- Les builds sont déclenchés automatiquement

## 🧪 7. Test du déploiement

1. **Testez l'API** : Visitez `https://your-backend-url.onrender.com/api/`
2. **Testez le frontend** : Visitez `https://your-app-name.netlify.app`
3. **Testez la connexion** : Essayez de vous connecter depuis le frontend

## 🐛 8. Dépannage

### Problèmes courants :

1. **Erreur CORS** : Vérifiez que les domaines sont bien configurés
2. **Erreur de base de données** : Vérifiez la DATABASE_URL
3. **Erreur de build** : Vérifiez les logs de build dans Render/Netlify
4. **Erreur 404** : Vérifiez que les routes sont bien configurées

### Logs utiles :
- Render.com : Dashboard > Votre service > Logs
- Netlify : Dashboard > Votre site > Deploys > Logs

## 📝 9. URLs finales

Après le déploiement, vous aurez :
- **Frontend** : `https://your-app-name.netlify.app`
- **Backend** : `https://your-backend-url.onrender.com`
- **API** : `https://your-backend-url.onrender.com/api/`

## 🔒 10. Sécurité

- Changez le SECRET_KEY en production
- Utilisez HTTPS en production
- Configurez les variables d'environnement sensibles
- Activez l'authentification à deux facteurs sur vos comptes

---

**Note** : Remplacez `your-app-name` et `your-backend-url` par les noms réels de vos services. 