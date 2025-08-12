#!/bin/bash

echo "🚀 Déploiement de l'Application de Réservation"
echo "=============================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que Git est configuré
if ! git config --get user.name > /dev/null 2>&1; then
    print_error "Git n'est pas configuré. Veuillez configurer votre nom et email Git."
    exit 1
fi

print_status "Git est configuré"

# Vérifier que le repository est connecté à GitHub
if ! git remote get-url origin > /dev/null 2>&1; then
    print_error "Aucun remote 'origin' trouvé. Veuillez connecter votre repository à GitHub."
    exit 1
fi

print_status "Repository GitHub connecté"

# Vérifier les modifications non commitées
if ! git diff-index --quiet HEAD --; then
    print_warning "Il y a des modifications non commitées."
    read -p "Voulez-vous les commiter maintenant? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Auto-commit before deployment"
        print_status "Modifications commitées"
    else
        print_error "Déploiement annulé. Veuillez commiter vos modifications."
        exit 1
    fi
fi

# Pousser vers GitHub
print_status "Poussage vers GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    print_status "Code poussé vers GitHub avec succès"
else
    print_error "Erreur lors du push vers GitHub"
    exit 1
fi

echo ""
echo "🎉 Déploiement déclenché !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Allez sur Render.com et créez votre service Django"
echo "2. Allez sur Netlify.com et créez votre site"
echo "3. Configurez les variables d'environnement"
echo "4. Testez votre application"
echo ""
echo "📖 Consultez DEPLOYMENT.md pour les instructions détaillées"
echo ""
echo "🔗 URLs attendues :"
echo "- Backend: https://your-app-name.onrender.com"
echo "- Frontend: https://your-app-name.netlify.app" 