# 🚀 Déploiement du Backend Django

## Problème actuel
- ✅ Frontend Vite : Déployé sur Vercel
- ❌ Backend Django : Local seulement
- ❌ Erreur : "Impossible de se connecter au serveur"

## Solutions disponibles

### **Option 1 : Railway (Recommandé - Gratuit)**

1. **Créez un compte** : https://railway.app/
2. **Connectez votre repo GitHub**
3. **Déployez automatiquement**

### **Option 2 : Render (Gratuit)**

1. **Créez un compte** : https://render.com/
2. **Nouveau Web Service**
3. **Connectez votre repo**

### **Option 3 : Heroku (Payant)**

1. **Créez un compte** : https://heroku.com/
2. **Déployez avec Git**

---

## 🛠️ Configuration pour le déploiement

### **Étape 1 : Préparer le backend**

```bash
cd server
```

### **Étape 2 : Créer un fichier Procfile**

```bash
echo "web: gunicorn reservation_project.wsgi:application" > Procfile
```

### **Étape 3 : Configurer les variables d'environnement**

Créez un fichier `.env` pour la production :

```env
DEBUG=False
SECRET_KEY=votre-clé-secrète
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=.vercel.app,.railway.app
CORS_ALLOWED_ORIGINS=https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app
```

### **Étape 4 : Mettre à jour settings.py**

```python
# settings_prod.py
import os
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']  # À configurer selon votre domaine

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app",
    "https://vercel.app",
]

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## 🚀 Déploiement sur Railway

### **Étape 1 : Préparer le repo**

```bash
# Dans le dossier server
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### **Étape 2 : Déployer sur Railway**

1. **Allez sur** : https://railway.app/
2. **"New Project"** → **"Deploy from GitHub repo"**
3. **Sélectionnez** votre repo
4. **Configurez** les variables d'environnement
5. **Déployez**

### **Étape 3 : Obtenir l'URL du backend**

Railway vous donnera une URL comme :
```
https://votre-app.railway.app
```

---

## 🔗 Mettre à jour le frontend

### **Étape 1 : Mettre à jour l'URL de l'API**

Dans `client/src/services/api.ts` :

```typescript
// Remplacer
const API_BASE_URL = 'http://localhost:8000/api';

// Par
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://votre-app.railway.app/api'
  : 'http://localhost:8000/api';
```

### **Étape 2 : Redéployer le frontend**

```bash
cd client
npx vercel --prod
```

---

## ✅ Résultat final

Après déploiement :
- **Frontend** : `https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app`
- **Backend** : `https://votre-app.railway.app`
- **API** : `https://votre-app.railway.app/api`

---

## 🐛 Dépannage

### **Erreur CORS**
```python
# Dans settings.py
CORS_ALLOW_ALL_ORIGINS = True  # Temporaire pour les tests
```

### **Erreur de base de données**
- Vérifiez les variables d'environnement
- Assurez-vous que la base de données est accessible

### **Erreur de migration**
```bash
python manage.py migrate
```

---

## 📞 Support

- **Railway Docs** : https://docs.railway.app/
- **Render Docs** : https://render.com/docs
- **Heroku Docs** : https://devcenter.heroku.com/ 