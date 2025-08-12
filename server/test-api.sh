#!/bin/bash

echo "🧪 Test de l'API après déploiement Railway..."

# Demander l'URL du backend
echo "🌐 Entrez l'URL de votre backend Railway (ex: https://votre-app.railway.app):"
read -r BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo "❌ URL non fournie. Exemple: https://votre-app.railway.app"
    exit 1
fi

echo ""
echo "🔍 Test de l'API sur: $BACKEND_URL"
echo ""

# Test 1: Endpoint principal
echo "📡 Test 1: Endpoint principal"
curl -s "$BACKEND_URL/api/" | head -5
echo ""
echo ""

# Test 2: Endpoint d'authentification
echo "🔐 Test 2: Endpoint d'authentification"
curl -s -X POST "$BACKEND_URL/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"phone":"test","password":"test"}' | head -5
echo ""
echo ""

# Test 3: Endpoint des hôtels
echo "🏨 Test 3: Endpoint des hôtels"
curl -s "$BACKEND_URL/api/hotels/" | head -5
echo ""
echo ""

# Test 4: Endpoint des appartements
echo "🏠 Test 4: Endpoint des appartements"
curl -s "$BACKEND_URL/api/apartments/" | head -5
echo ""
echo ""

echo "✅ Tests terminés !"
echo ""
echo "📋 Résultats :"
echo "- Si vous voyez du JSON, l'API fonctionne"
echo "- Si vous voyez des erreurs, vérifiez la configuration"
echo ""
echo "🔗 URL de votre API: $BACKEND_URL/api/"
echo "🌐 URL de votre frontend: https://client-9ivvs69wl-moussa-bas-projects-5b2e16f9.vercel.app" 