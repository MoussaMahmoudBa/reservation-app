# 🏨 Application de Réservation d'Hôtels et d'Appartements

Une application web complète pour la réservation d'hôtels et d'appartements, construite avec React (Vite) et Django.

## 🚀 Déploiement

### **Frontend (Vercel)**
- **URL** : https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app
- **Technologie** : React + Vite + TypeScript
- **Déploiement** : Vercel

### **Backend (Railway)**
- **URL** : `https://votre-app.railway.app` (à configurer)
- **Technologie** : Django + Django REST Framework
- **Déploiement** : Railway

## 📁 Structure du projet

```
Reservation/
├── client/                 # Frontend React + Vite
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── server/                 # Backend Django
│   ├── reservation_project/
│   ├── hotels/
│   ├── apartments/
│   ├── users/
│   ├── reservations/
│   └── manage.py
├── README.md
└── .gitignore
```

## 🛠️ Technologies utilisées

### **Frontend**
- **React 18** avec TypeScript
- **Vite** pour le build et le développement
- **React Router** pour la navigation
- **Axios** pour les requêtes API
- **Tailwind CSS** pour le styling
- **Lucide React** pour les icônes

### **Backend**
- **Django 4.2** avec Python 3.11
- **Django REST Framework** pour l'API
- **PostgreSQL** pour la base de données
- **JWT** pour l'authentification
- **Cloudinary** pour le stockage des images
- **CORS** pour la communication cross-origin

## 🚀 Installation locale

### **Prérequis**
- Node.js 18+
- Python 3.11+
- PostgreSQL

### **Frontend**
```bash
cd client
npm install
npm run dev
```

### **Backend**
```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🌐 Déploiement

### **Frontend sur Vercel**
```bash
cd client
npx vercel --prod
```

### **Backend sur Railway**
1. Créez un compte sur https://railway.app/
2. Connectez votre repository GitHub
3. Déployez le dossier `server/`
4. Configurez les variables d'environnement

## 🔧 Configuration

### **Variables d'environnement Backend**
```env
SECRET_KEY=votre-clé-secrète
DEBUG=False
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://votre-frontend.vercel.app
```

### **Variables d'environnement Frontend**
```env
VITE_API_URL=https://votre-backend.railway.app/api
```

## 📱 Fonctionnalités

### **Utilisateurs**
- ✅ Inscription et connexion
- ✅ Gestion de profil
- ✅ Réinitialisation de mot de passe

### **Hôtels**
- ✅ Liste des hôtels
- ✅ Détails d'un hôtel
- ✅ Recherche et filtres
- ✅ Système de réservation

### **Appartements**
- ✅ Liste des appartements
- ✅ Détails d'un appartement
- ✅ Recherche et filtres
- ✅ Système de réservation

### **Administration**
- ✅ Dashboard admin
- ✅ Gestion des utilisateurs
- ✅ Gestion des hôtels et appartements
- ✅ Gestion des réservations

## 🔗 API Endpoints

### **Authentification**
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/logout/` - Déconnexion

### **Hôtels**
- `GET /api/hotels/` - Liste des hôtels
- `GET /api/hotels/{id}/` - Détails d'un hôtel
- `POST /api/hotels/` - Créer un hôtel (admin)

### **Appartements**
- `GET /api/apartments/` - Liste des appartements
- `GET /api/apartments/{id}/` - Détails d'un appartement
- `POST /api/apartments/` - Créer un appartement (admin)

### **Réservations**
- `GET /api/reservations/` - Liste des réservations
- `POST /api/reservations/hotel/` - Réserver un hôtel
- `POST /api/reservations/apartment/` - Réserver un appartement

## 🎯 Développement

### **Scripts utiles**
```bash
# Démarrer le frontend
cd client && npm run dev

# Démarrer le backend
cd server && python manage.py runserver

# Tests frontend
cd client && npm test

# Tests backend
cd server && python manage.py test
```

## 📞 Support

- **Documentation Vercel** : https://vercel.com/docs
- **Documentation Railway** : https://docs.railway.app/
- **Documentation Django** : https://docs.djangoproject.com/

## 📄 Licence

Ce projet est sous licence MIT. 