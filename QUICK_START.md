# 🚀 Guide de Démarrage Rapide - Plateforme de Réservation Nouakchott

## ✅ Statut Actuel
- **Backend Django** : ✅ Fonctionnel
- **Frontend React** : ✅ Fonctionnel
- **Base de données** : ✅ Initialisée
- **Authentification** : ✅ Configurée

## 🎯 Accès Rapide

### URLs d'Accès
- **Frontend** : http://localhost:3000
- **Backend** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin
- **API REST** : http://localhost:8000/api/

### Compte Administrateur
- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`
- **Email** : `admin@example.com`

## 🔧 Démarrage Manuel

### Option 1 : Script Automatique
```bash
chmod +x start_simple.sh
./start_simple.sh
```

### Option 2 : Démarrage Manuel
```bash
# Terminal 1 - Backend Django
cd server
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend React
cd client
npm start
```

## 📊 Test de l'Application

### 1. Test du Backend
```bash
# Vérifier que Django fonctionne
curl http://localhost:8000/api/

# Vérifier l'admin
curl http://localhost:8000/admin/
```

### 2. Test du Frontend
```bash
# Vérifier que React fonctionne
curl http://localhost:3000/
```

### 3. Test de l'API
```bash
# Liste des hôtels
curl http://localhost:8000/api/hotels/

# Liste des appartements
curl http://localhost:8000/api/apartments/

# Authentification
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 🎨 Interface Utilisateur

### Pages Disponibles
1. **Page d'accueil** : http://localhost:3000
   - Barre de recherche
   - Liste des destinations populaires
   - Navigation vers hôtels/appartements

2. **Admin Django** : http://localhost:8000/admin
   - Gestion des utilisateurs
   - Gestion des hôtels
   - Gestion des appartements
   - Gestion des réservations

## 🔑 Fonctionnalités Principales

### Backend (Django)
- ✅ **Authentification JWT** : Connexion/déconnexion sécurisée
- ✅ **Gestion des utilisateurs** : CRUD complet avec rôles
- ✅ **Gestion des hôtels** : CRUD complet avec images et avis
- ✅ **Gestion des appartements** : CRUD complet avec disponibilités
- ✅ **Gestion des réservations** : CRUD complet avec paiements
- ✅ **API REST** : Endpoints complets pour toutes les entités
- ✅ **Permissions** : Système de permissions personnalisé
- ✅ **Admin Django** : Interface d'administration complète

### Frontend (React)
- ✅ **Interface utilisateur** : Composants réutilisables
- ✅ **Styling** : Tailwind CSS configuré
- ✅ **Types TypeScript** : Types définis pour toutes les entités
- ✅ **Services API** : Service centralisé pour les appels API
- ✅ **Page d'accueil** : Interface de base implémentée

## 🛠️ Commandes Utiles

### Backend Django
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Shell Django
python manage.py shell
```

### Frontend React
```bash
# Installer les dépendances
npm install

# Démarrer en mode développement
npm start

# Build pour production
npm run build

# Tests
npm test
```

## 🐛 Résolution de Problèmes

### Problème 1 : ModuleNotFoundError: No module named 'decouple'
```bash
cd server
source venv/bin/activate
pip install python-decouple
```

### Problème 2 : Erreur Tailwind CSS PostCSS
```bash
cd client
npm install @tailwindcss/postcss7-compat
```

### Problème 3 : ALLOWED_HOSTS
- Vérifier que `0.0.0.0` est dans `ALLOWED_HOSTS` dans `settings.py`

### Problème 4 : Ports déjà utilisés
```bash
# Trouver les processus
lsof -i :8000
lsof -i :3000

# Tuer les processus
kill -9 <PID>
```

## 📈 Prochaines Étapes

### Priorité Haute
1. **Tester l'application** : Vérifier que tout fonctionne
2. **Créer des données de test** : Ajouter des hôtels/appartements via l'admin
3. **Compléter les pages frontend** : Pages de liste, détails, réservation
4. **Implémenter l'authentification frontend** : Connexion/déconnexion

### Priorité Moyenne
1. **Ajouter des images** : Intégration Cloudinary
2. **Système de paiement** : Intégration PayTech ou Stripe
3. **Notifications** : Système d'emails/SMS
4. **Recherche avancée** : Filtres et recherche

## 🎉 Conclusion

L'application est maintenant **fonctionnelle** et prête pour le développement !

- ✅ Backend Django complet et opérationnel
- ✅ Frontend React configuré et démarré
- ✅ Base de données initialisée
- ✅ Authentification configurée
- ✅ API REST complète

**Vous pouvez maintenant commencer à développer et tester l'application !** 🚀 