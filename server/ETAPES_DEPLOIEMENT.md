# 🚀 Étapes de Déploiement Railway

## ✅ Préparation terminée !

Votre backend Django est maintenant prêt pour le déploiement sur Railway.

---

## 🔑 Informations importantes

### **Clé secrète Django générée :**
```
h_0=og0(t7_1brufq7wxzl_lh*fbgcxf=ifj(s*7r7*^2an18@
```

### **URL de votre frontend Vercel :**
```
https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app
```

---

## 📋 Étapes à suivre maintenant

### **1. Créer un compte Railway**
- Allez sur : https://railway.app/
- Cliquez sur "Get Started"
- Connectez-vous avec GitHub

### **2. Créer un nouveau projet**
- Cliquez sur "New Project"
- Choisissez "Deploy from GitHub repo"
- Sélectionnez votre repository
- **Important** : Choisissez le dossier `server` (pas le root)

### **3. Ajouter une base de données**
- Dans votre projet Railway
- Cliquez sur "New"
- Choisissez "Database" → "PostgreSQL"
- Attendez que la base de données soit créée

### **4. Configurer les variables d'environnement**
Dans la section "Variables" de votre projet Railway, ajoutez :

```env
# Django
SECRET_KEY=h_0=og0(t7_1brufq7wxzl_lh*fbgcxf=ifj(s*7r7*^2an18@
DEBUG=False
DJANGO_SETTINGS_MODULE=reservation_project.settings_prod

# CORS (pour permettre l'accès depuis Vercel)
CORS_ALLOWED_ORIGINS=https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app

# Base de données (ajouté automatiquement par Railway)
DATABASE_URL=postgresql://... (automatique)
```

### **5. Déployer**
- Railway déploiera automatiquement
- Attendez que le build soit terminé
- Vérifiez les logs pour les erreurs

---

## 🌐 Après le déploiement

### **Obtenir l'URL du backend**
Railway vous donnera une URL comme :
```
https://votre-app.railway.app
```

### **Tester l'API**
```bash
curl https://votre-app.railway.app/api/
```

### **Mettre à jour le frontend**
Dans `client/src/services/api.ts`, remplacez :
```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://votre-app.railway.app/api'  // Votre URL Railway
  : 'http://localhost:8000/api';
```

### **Redéployer le frontend**
```bash
cd client
npx vercel --prod
```

---

## 🎯 Résultat final

Après toutes ces étapes :
- **Frontend** : `https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app`
- **Backend** : `https://votre-app.railway.app`
- **API** : `https://votre-app.railway.app/api/`

Votre application sera entièrement fonctionnelle ! 🚀

---

## 🆘 Besoin d'aide ?

- **Guide complet** : `RAILWAY_DEPLOYMENT.md`
- **Documentation Railway** : https://docs.railway.app/
- **Support Railway** : https://railway.app/support 