#!/bin/bash

echo "🚀 Déploiement avec migrations Railway"
echo "======================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le dossier server/"
    exit 1
fi

echo "📋 Préparation du déploiement..."

# Ajouter tous les fichiers
git add .

# Commiter les changements
git commit -m "Add: Railway migrations and deployment scripts"

# Pousser vers GitHub
echo "📤 Poussée vers GitHub..."
git push

echo "✅ Déploiement lancé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Railway va automatiquement redéployer"
echo "2. Les migrations seront exécutées automatiquement"
echo "3. Attendez 2-3 minutes puis testez l'API"
echo ""
echo "🔗 URL de test : https://web-production-31bc.up.railway.app/api/"
echo "🌐 Frontend : https://client-84jdcuirb-moussa-bas-projects-5b2e16f9.vercel.app" 