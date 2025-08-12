#!/usr/bin/env python
import os

def create_env_file():
    """Crée le fichier .env avec les paramètres PostgreSQL"""
    env_content = """DB_ENGINE=postgres
DB_NAME=reservation_db
DB_USER=postgres
DB_PASSWORD=Moussa123
DB_HOST=localhost
DB_PORT=5433
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Fichier .env créé avec succès: {env_file_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .env: {e}")
        return False

def check_env_file():
    """Vérifie si le fichier .env existe"""
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file_path):
        print(f"✅ Fichier .env existe déjà: {env_file_path}")
        return True
    else:
        print(f"❌ Fichier .env manquant: {env_file_path}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CONFIGURATION DE L'ENVIRONNEMENT")
    print("=" * 50)
    
    if not check_env_file():
        print("Création du fichier .env...")
        create_env_file()
    
    print("\nConfiguration terminée !")
    print("Vous pouvez maintenant démarrer le serveur avec:")
    print("python manage.py runserver 0.0.0.0:8000") 