#!/bin/bash

# Script de démarrage pour le client React avec Vite
echo "🎨 Démarrage du client React avec Vite..."

# Aller dans le répertoire du client
cd client

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
if [ ! -d "node_modules" ]; then
    echo "📥 Installation des dépendances..."
    npm install
fi

# Démarrer le serveur de développement Vite
echo "⚡ Démarrage du client React avec Vite sur http://localhost:3000"
echo ""
echo "🚀 Avantages de Vite :"
echo "   - Hot reload ultra-rapide"
echo "   - Build optimisé"
echo "   - Développement plus fluide"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

npm run dev 