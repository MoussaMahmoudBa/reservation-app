# 🚀 Déploiement Rapide - Application de Réservation

## 📋 Prérequis

- ✅ Compte GitHub avec votre code
- ✅ Compte Render.com (gratuit)
- ✅ Compte Netlify (gratuit)
- ✅ Compte Cloudinary (optionnel, pour les images)

## ⚡ Déploiement en 5 minutes

### 1️⃣ Backend (Django) sur Render.com

1. **Allez sur [render.com](https://render.com)**
2. **Créez une base de données PostgreSQL** :
   - New + → PostgreSQL
   - Name: `reservation-postgres`
   - Plan: Free
   - Create Database

3. **Déployez le service Django** :
   - New + → Web Service
   - Connectez votre repo GitHub
   - Root Directory: `server`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn reservation_project.wsgi:application`
   - Plan: Free

4. **Variables d'environnement** :
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=false
   DATABASE_URL=postgres://... (copié depuis votre DB)
   ```

### 2️⃣ Frontend (React) sur Netlify

1. **Allez sur [netlify.com](https://netlify.com)**
2. **New site from Git** :
   - Connectez votre repo GitHub
   - Base directory: `client`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Variables d'environnement** :
   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api
   ```

### 3️⃣ Configuration CORS

Dans `server/reservation_project/settings.py`, ajoutez votre domaine Netlify :

```python
CORS_ALLOWED_ORIGINS = [
    # ... autres domaines ...
    "https://your-app-name.netlify.app",
]
```

## 🔧 Script de déploiement automatique

```bash
./deploy.sh
```

Ce script va :
- ✅ Vérifier Git
- ✅ Commiter les changements
- ✅ Pousser vers GitHub
- ✅ Déclencher le déploiement automatique

## 📱 URLs finales

- **Frontend** : `https://your-app-name.netlify.app`
- **Backend** : `https://your-backend-url.onrender.com`
- **API** : `https://your-backend-url.onrender.com/api/`

## 🐛 Dépannage rapide

| Problème | Solution |
|----------|----------|
| Erreur CORS | Vérifiez les domaines dans settings.py |
| Erreur DB | Vérifiez DATABASE_URL dans Render |
| Build échoue | Vérifiez les logs dans Render/Netlify |
| 404 | Vérifiez les routes API |

## 📖 Documentation complète

Consultez `DEPLOYMENT.md` pour les instructions détaillées.

---

**💡 Astuce** : Utilisez le script `./deploy.sh` pour automatiser le processus ! 