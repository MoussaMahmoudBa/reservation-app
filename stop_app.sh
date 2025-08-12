#!/bin/bash

echo "🛑 Arrêt de l'application de réservation..."

# Arrêter le serveur Django
if pgrep -f "python manage.py runserver" > /dev/null; then
    echo "🐍 Arrêt du serveur Django..."
    pkill -f "python manage.py runserver"
    echo "✅ Serveur Django arrêté"
else
    echo "ℹ️  Le serveur Django n'était pas en cours d'exécution"
fi

# Arrêter le client React
if pgrep -f "react-scripts" > /dev/null; then
    echo "⚛️  Arrêt du client React..."
    pkill -f "react-scripts"
    echo "✅ Client React arrêté"
else
    echo "ℹ️  Le client React n'était pas en cours d'exécution"
fi

# Arrêter tous les processus npm
if pgrep -f "npm start" > /dev/null; then
    echo "📦 Arrêt des processus npm..."
    pkill -f "npm start"
    echo "✅ Processus npm arrêtés"
fi

echo ""
echo "✅ Application arrêtée avec succès!" 