# 🚀 Guide Interactif - Déploiement Railway

## 📋 Checklist de déploiement

### ✅ Étape 1 : Préparation (TERMINÉE)
- [x] Fichiers de configuration créés
- [x] Repository Git initialisé
- [x] Clé secrète Django générée
- [x] Code commité

### 🔄 Étape 2 : Créer un compte Railway
- [ ] Aller sur https://railway.app/
- [ ] Cliquer sur "Get Started"
- [ ] Se connecter avec GitHub
- [ ] Autoriser Railway

### 🔄 Étape 3 : Créer un nouveau projet
- [ ] Cliquer sur "New Project"
- [ ] Choisir "Deploy from GitHub repo"
- [ ] Sélectionner votre repository
- [ ] **IMPORTANT** : Choisir le dossier `server` (pas le root)

### 🔄 Étape 4 : Ajouter une base de données
- [ ] Dans le projet Railway
- [ ] Cliquer sur "New"
- [ ] Choisir "Database" → "PostgreSQL"
- [ ] Attendre la création

### 🔄 Étape 5 : Configurer les variables d'environnement
- [ ] Aller dans "Variables"
- [ ] Ajouter les variables suivantes :

```env
# Django
SECRET_KEY=h_0=og0(t7_1brufq7wxzl_lh*fbgcxf=ifj(s*7r7*^2an18@
DEBUG=False
DJANGO_SETTINGS_MODULE=reservation_project.settings_prod

# CORS
CORS_ALLOWED_ORIGINS=https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app

# Base de données (ajouté automatiquement)
DATABASE_URL=postgresql://... (automatique)
```

### 🔄 Étape 6 : Déployer
- [ ] Railway déploiera automatiquement
- [ ] Attendre la fin du build
- [ ] Vérifier les logs

### 🔄 Étape 7 : Obtenir l'URL du backend
- [ ] Copier l'URL fournie par Railway
- [ ] Tester l'API

### 🔄 Étape 8 : Mettre à jour le frontend
- [ ] Modifier l'URL de l'API
- [ ] Redéployer sur Vercel

---

## 🎯 Informations importantes

### **URL de votre frontend :**
```
https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app
```

### **Clé secrète Django :**
```
h_0=og0(t7_1brufq7wxzl_lh*fbgcxf=ifj(s*7r7*^2an18@
```

### **Structure du repository :**
```
Reservation/
├── client/          # Frontend Vite (déjà déployé sur Vercel)
└── server/          # Backend Django (à déployer sur Railway)
```

---

## 🚨 Points d'attention

### **1. Choisir le bon dossier**
- ✅ Sélectionner le dossier `server`
- ❌ Ne pas sélectionner le dossier root

### **2. Variables d'environnement**
- ✅ Copier exactement la clé secrète
- ✅ Vérifier l'URL du frontend Vercel
- ✅ Laisser DATABASE_URL automatique

### **3. Base de données**
- ✅ Attendre que PostgreSQL soit créé
- ✅ Vérifier que les variables sont ajoutées

---

## 🆘 En cas de problème

### **Erreur de build**
- Vérifier les logs Railway
- S'assurer que tous les fichiers sont présents
- Vérifier les variables d'environnement

### **Erreur de base de données**
- Vérifier que PostgreSQL est créé
- Vérifier les variables DATABASE_URL
- Exécuter les migrations

### **Erreur CORS**
- Vérifier CORS_ALLOWED_ORIGINS
- Ajouter votre domaine Vercel

---

## 📞 Support

- **Documentation Railway** : https://docs.railway.app/
- **Support Railway** : https://railway.app/support
- **Discord Railway** : https://discord.gg/railway

---

## 🎉 Résultat attendu

Après déploiement :
- **Frontend** : `https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app`
- **Backend** : `https://votre-app.railway.app`
- **API** : `https://votre-app.railway.app/api/`

Votre application sera entièrement fonctionnelle ! 🚀 