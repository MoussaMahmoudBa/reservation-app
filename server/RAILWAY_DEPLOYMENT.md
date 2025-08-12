# 🚀 Déploiement Railway - Guide Complet

## 📋 Prérequis

- ✅ Compte GitHub
- ✅ Code backend Django prêt
- ✅ Fichiers de configuration créés

## 🛠️ Fichiers de configuration créés

### **Procfile**
```
web: gunicorn reservation_project.wsgi:application --bind 0.0.0.0:$PORT
```

### **runtime.txt**
```
python-3.11.7
```

### **settings_prod.py**
Configuration de production avec :
- CORS configuré pour Vercel
- Base de données PostgreSQL
- Sécurité HTTPS

---

## 🚀 Étapes de déploiement

### **Étape 1 : Préparer le repository**

```bash
cd server
./deploy-railway.sh
```

### **Étape 2 : Créer un compte Railway**

1. **Allez sur** : https://railway.app/
2. **Cliquez** sur "Get Started"
3. **Choisissez** "Continue with GitHub"
4. **Autorisez** Railway à accéder à votre GitHub

### **Étape 3 : Créer un nouveau projet**

1. **Cliquez** sur "New Project"
2. **Choisissez** "Deploy from GitHub repo"
3. **Sélectionnez** votre repository
4. **Choisissez** le dossier `server` (pas le root)

### **Étape 4 : Configurer la base de données**

1. **Cliquez** sur "New"
2. **Choisissez** "Database" → "PostgreSQL"
3. **Attendez** que la base de données soit créée
4. **Notez** les variables d'environnement

### **Étape 5 : Configurer les variables d'environnement**

Dans votre projet Railway, allez dans "Variables" et ajoutez :

```env
# Base de données (automatiquement ajouté par Railway)
DATABASE_URL=postgresql://...

# Django
SECRET_KEY=votre-clé-secrète-très-longue
DEBUG=False
DJANGO_SETTINGS_MODULE=reservation_project.settings_prod

# CORS
CORS_ALLOWED_ORIGINS=https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app

# Cloudinary (optionnel)
CLOUDINARY_CLOUD_NAME=votre-cloud-name
CLOUDINARY_API_KEY=votre-api-key
CLOUDINARY_API_SECRET=votre-api-secret
```

### **Étape 6 : Déployer**

1. **Railway déploiera automatiquement**
2. **Attendez** que le build soit terminé
3. **Vérifiez** les logs pour les erreurs

---

## 🔧 Configuration avancée

### **Variables d'environnement importantes**

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DATABASE_URL` | URL de la base de données | `postgresql://user:pass@host:port/db` |
| `SECRET_KEY` | Clé secrète Django | `django-insecure-...` |
| `DEBUG` | Mode debug | `False` |
| `DJANGO_SETTINGS_MODULE` | Module de paramètres | `reservation_project.settings_prod` |

### **Générer une clé secrète**

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🌐 Obtenir l'URL du backend

Après déploiement, Railway vous donnera une URL comme :
```
https://votre-app.railway.app
```

Votre API sera accessible sur :
```
https://votre-app.railway.app/api/
```

---

## 🔗 Mettre à jour le frontend

### **Étape 1 : Mettre à jour l'URL de l'API**

Dans `client/src/services/api.ts` :

```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://votre-app.railway.app/api'  // Remplacez par votre URL Railway
  : 'http://localhost:8000/api';
```

### **Étape 2 : Redéployer le frontend**

```bash
cd client
npx vercel --prod
```

---

## 🐛 Dépannage

### **Erreur de build**
- Vérifiez les logs Railway
- Assurez-vous que tous les fichiers sont présents
- Vérifiez les variables d'environnement

### **Erreur de base de données**
- Vérifiez que PostgreSQL est créé
- Vérifiez les variables DATABASE_URL
- Exécutez les migrations : `python manage.py migrate`

### **Erreur CORS**
- Vérifiez CORS_ALLOWED_ORIGINS
- Ajoutez votre domaine Vercel

### **Erreur de port**
- Railway utilise la variable $PORT automatiquement
- Vérifiez le Procfile

---

## ✅ Vérification du déploiement

### **Test de l'API**
```bash
curl https://votre-app.railway.app/api/
```

### **Test de l'authentification**
```bash
curl -X POST https://votre-app.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"phone":"test","password":"test"}'
```

---

## 📞 Support

- **Documentation Railway** : https://docs.railway.app/
- **Support Railway** : https://railway.app/support
- **Discord Railway** : https://discord.gg/railway

---

## 🎉 Résultat final

Après déploiement :
- **Backend** : `https://votre-app.railway.app`
- **API** : `https://votre-app.railway.app/api/`
- **Frontend** : `https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app`

Votre application sera entièrement fonctionnelle ! 🚀 