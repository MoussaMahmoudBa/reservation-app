#!/usr/bin/env python3
"""
Script pour exécuter les migrations Django sur Railway
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings_prod')

# Initialiser Django
django.setup()

from django.core.management import execute_from_command_line

def main():
    print("🔧 Exécution des migrations Django sur Railway...")
    print("=" * 50)
    
    try:
        # Exécuter les migrations
        print("📋 Exécution de makemigrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        print("📋 Exécution de migrate...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations terminées avec succès !")
        
        # Créer un superuser si demandé
        print("\n👤 Voulez-vous créer un superuser ? (y/n): ", end="")
        response = input().lower().strip()
        
        if response == 'y':
            print("📋 Création du superuser...")
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("✅ Superuser créé avec succès !")
        
        print("\n🎉 Configuration terminée !")
        
    except Exception as e:
        print(f"❌ Erreur lors des migrations : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 