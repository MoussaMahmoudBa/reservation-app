#!/usr/bin/env python3
"""
Script pour exécuter des commandes Django sur Railway
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

def run_migrations():
    """Exécuter les migrations"""
    print("📋 Exécution des migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Créer un superuser"""
    print("👤 Création du superuser...")
    execute_from_command_line(['manage.py', 'createsuperuser'])

def collect_static():
    """Collecter les fichiers statiques"""
    print("📁 Collecte des fichiers statiques...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

def main():
    print("🔧 Commandes Django pour Railway")
    print("=" * 40)
    print("1. Exécuter les migrations")
    print("2. Créer un superuser")
    print("3. Collecter les fichiers statiques")
    print("4. Tout exécuter")
    print("5. Quitter")
    
    while True:
        choice = input("\nChoisissez une option (1-5): ").strip()
        
        if choice == '1':
            run_migrations()
        elif choice == '2':
            create_superuser()
        elif choice == '3':
            collect_static()
        elif choice == '4':
            run_migrations()
            collect_static()
            print("✅ Toutes les commandes exécutées !")
        elif choice == '5':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide. Veuillez choisir 1-5.")

if __name__ == "__main__":
    main() 