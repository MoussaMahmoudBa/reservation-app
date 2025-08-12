# Application de Réservation

Application de réservation d'hôtels et d'appartements développée avec React (Vite) et Django.

## 🚀 Technologies

- **Frontend** : React, TypeScript, Vite, Tailwind CSS
- **Backend** : Django, Django REST Framework, PostgreSQL
- **Authentification** : JWT

## 📁 Structure du Projet

```
Reservation/
├── client/          # Frontend React (Vite)
└── server/          # Backend Django
```

## 🛠️ Installation

### Prérequis
- Node.js (v16+)
- Python (v3.8+)
- PostgreSQL

### Frontend (React + Vite)

```bash
cd client
npm install
npm run dev
```

Le frontend sera accessible sur : http://localhost:3000

### Backend (Django)

```bash
cd server
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Le backend sera accessible sur : http://localhost:8000

## 🔧 Scripts Utiles

### Démarrer l'application complète
```bash
./start.sh
```

### Démarrer uniquement le frontend
```bash
./start_client.sh
```

### Démarrer uniquement le backend
```bash
./start_server.sh
```

## 📚 Documentation

- [Guide d'installation](INSTALLATION.md)
- [Statut du projet](PROJECT_STATUS.md)
- [Résumé du projet](PROJECT_SUMMARY.md)

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request 