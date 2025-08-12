#!/bin/bash

# Script de démarrage pour le client React
echo "🎨 Démarrage du client React..."

# Aller dans le répertoire du client
cd client

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
if [ ! -d "node_modules" ]; then
    echo "📥 Installation des dépendances..."
    npm install
fi

# Démarrer le serveur de développement
echo "🌐 Démarrage du client React sur http://localhost:3000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

npm start 