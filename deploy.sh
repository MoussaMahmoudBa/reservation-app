#!/bin/bash

echo "🚀 Déploiement de l'application Reservation..."

# 1. Build du frontend
echo "📦 Build du frontend React..."
cd client
npm run build
cd ..

# 2. Collecte des fichiers statiques Django
echo "📦 Collecte des fichiers statiques Django..."
cd server
python manage.py collectstatic --noinput
cd ..

echo "✅ Déploiement terminé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Poussez le code vers votre repository Git"
echo "2. Connectez-vous à Railway ou Render"
echo "3. Créez un nouveau projet"
echo "4. Connectez votre repository"
echo "5. Configurez les variables d'environnement"
echo "6. Déployez !" 