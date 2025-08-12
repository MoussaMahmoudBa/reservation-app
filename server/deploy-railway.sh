#!/bin/bash

echo "🚀 Préparation du déploiement Railway..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire server."
    exit 1
fi

# Vérifier que Git est initialisé
if [ ! -d ".git" ]; then
    echo "📦 Initialisation de Git..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
fi

echo "✅ Préparation terminée !"
echo ""
echo "📋 Étapes suivantes :"
echo "1. Allez sur https://railway.app/"
echo "2. Créez un compte ou connectez-vous"
echo "3. Cliquez sur 'New Project'"
echo "4. Choisissez 'Deploy from GitHub repo'"
echo "5. Sélectionnez votre repository"
echo "6. Railway déploiera automatiquement"
echo ""
echo "🔧 Configuration nécessaire :"
echo "- Ajoutez une base de données PostgreSQL"
echo "- Configurez les variables d'environnement"
echo "- Déployez le service web"
echo ""
echo "📖 Guide complet : https://docs.railway.app/" 