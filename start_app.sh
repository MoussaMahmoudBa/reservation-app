#!/bin/bash

echo "🚀 Démarrage de l'application de réservation..."
echo "================================================"

# Démarrer le serveur Django (backend)
echo "📡 Démarrage du serveur Django (Backend)..."
cd server
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!
cd ..

# Attendre un peu que Django démarre
sleep 3

# Démarrer le client React (frontend)
echo "🎨 Démarrage du client React (Frontend)..."
cd client
npm start &
REACT_PID=$!
cd ..

echo ""
echo "✅ Application démarrée avec succès !"
echo "================================================"
echo "🌐 Frontend (React): http://localhost:3000"
echo "🔧 Backend (Django): http://localhost:8000"
echo "📊 API Endpoints: http://localhost:8000/api/"
echo "👤 Admin Panel: http://localhost:8000/admin/"
echo ""
echo "👤 Utilisateur admin: MoussaAdmin"
echo "📧 Email: admin@reservation.com"
echo "📱 Téléphone: +22241240690"
echo ""
echo "🛑 Pour arrêter les serveurs: Ctrl+C"
echo "================================================"

# Attendre que l'utilisateur arrête
wait 