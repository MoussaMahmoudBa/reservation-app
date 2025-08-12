#!/usr/bin/env python
import os
import sys
import subprocess

# Configuration des variables d'environnement pour PostgreSQL
os.environ['DB_ENGINE'] = 'postgres'
os.environ['DB_NAME'] = 'reservation_db'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'Moussa123'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5433'

print("=" * 60)
print("DÉMARRAGE DU SERVEUR DJANGO AVEC POSTGRESQL")
print("=" * 60)
print(f"Base de données: {os.environ['DB_NAME']}")
print(f"Utilisateur: {os.environ['DB_USER']}")
print(f"Hôte: {os.environ['DB_HOST']}:{os.environ['DB_PORT']}")
print("=" * 60)

# Démarrer le serveur Django
try:
    subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], check=True)
except KeyboardInterrupt:
    print("\n🛑 Serveur arrêté par l'utilisateur")
except subprocess.CalledProcessError as e:
    print(f"❌ Erreur lors du démarrage du serveur: {e}")
except Exception as e:
    print(f"❌ Erreur inattendue: {e}") 