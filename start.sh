#!/bin/bash

echo "🏨 Démarrage de la Plateforme de Réservation Nouakchott"
echo "=================================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Vérifications des prérequis terminées"

# Démarrer le backend Django
echo "🚀 Démarrage du backend Django..."
cd server

# Activer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur si nécessaire
echo "👤 Création d'un superutilisateur..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Démarrer le serveur Django
echo "🌐 Démarrage du serveur Django sur http://localhost:8000"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Démarrer le frontend React
echo "🎨 Démarrage du frontend React..."
cd ../client

# Installer les dépendances
echo "📦 Installation des dépendances Node.js..."
npm install

# Démarrer le serveur React
echo "🌐 Démarrage du serveur React sur http://localhost:3000"
npm start &
REACT_PID=$!

echo ""
echo "🎉 Application démarrée avec succès!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "👨‍💼 Admin: http://localhost:8000/admin (admin/admin123)"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les serveurs"

# Fonction pour nettoyer les processus
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    kill $DJANGO_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre que les processus se terminent
wait 