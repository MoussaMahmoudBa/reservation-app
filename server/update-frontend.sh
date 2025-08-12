#!/bin/bash

echo "🔄 Mise à jour du frontend avec l'URL du backend..."

# Demander l'URL du backend
echo "🌐 Entrez l'URL de votre backend Railway (ex: https://votre-app.railway.app):"
read -r BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo "❌ URL non fournie. Exemple: https://votre-app.railway.app"
    exit 1
fi

# Aller dans le dossier client
cd ../client

if [ ! -f "src/services/api.ts" ]; then
    echo "❌ Erreur: Fichier api.ts non trouvé dans le dossier client"
    exit 1
fi

echo "📝 Mise à jour de l'URL de l'API..."

# Créer une sauvegarde
cp src/services/api.ts src/services/api.ts.backup

# Mettre à jour l'URL de l'API
sed -i "s|https://votre-backend-url.railway.app/api|${BACKEND_URL}/api|g" src/services/api.ts

echo "✅ URL de l'API mise à jour !"
echo ""

# Vérifier le changement
echo "📋 Nouvelle configuration :"
grep -A 2 -B 2 "API_BASE_URL" src/services/api.ts
echo ""

echo "🚀 Redéploiement sur Vercel..."
echo "📋 Commandes à exécuter :"
echo "cd client"
echo "npx vercel --prod"
echo ""

echo "🎯 Après redéploiement :"
echo "- Frontend : https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app"
echo "- Backend : $BACKEND_URL"
echo "- API : $BACKEND_URL/api/"
echo ""

echo "✅ Mise à jour terminée !" 