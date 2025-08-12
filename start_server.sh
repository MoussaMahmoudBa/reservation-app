#!/bin/bash

echo "🚀 Démarrage du serveur Django..."
echo "=================================="

cd server
source venv/bin/activate

echo "✅ Environnement virtuel activé"
echo "✅ Configuration PostgreSQL chargée"
echo "🌐 Serveur démarré sur: http://localhost:8000"
echo ""

python manage.py runserver 0.0.0.0:8000 