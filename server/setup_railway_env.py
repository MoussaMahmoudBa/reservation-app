#!/usr/bin/env python3
"""
Script pour configurer les variables d'environnement Railway
"""

import secrets
import string

def generate_secret_key(length=50):
    """Génère une clé secrète Django sécurisée"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔧 Configuration des variables d'environnement Railway")
    print("=" * 50)
    
    # Générer une clé secrète
    secret_key = generate_secret_key()
    
    print("\n📋 Variables d'environnement à configurer dans Railway :")
    print("-" * 50)
    
    print(f"SECRET_KEY={secret_key}")
    print("DB_NAME=railway")
    print("DB_USER=postgres")
    print("DB_PASSWORD=<votre_mot_de_passe_postgres>")
    print("DB_HOST=<votre_host_postgres_railway>")
    print("DB_PORT=5432")
    
    print("\n📝 Instructions :")
    print("1. Allez dans votre dashboard Railway")
    print("2. Cliquez sur votre service Django")
    print("3. Allez dans 'Variables'")
    print("4. Ajoutez chaque variable ci-dessus")
    print("5. Pour DB_PASSWORD et DB_HOST, utilisez les valeurs de votre base PostgreSQL Railway")
    
    print("\n🔗 Comment trouver les infos PostgreSQL :")
    print("1. Dans Railway, cliquez sur votre service PostgreSQL")
    print("2. Allez dans 'Connect'")
    print("3. Copiez les informations de connexion")
    
    print(f"\n💾 Clé secrète générée : {secret_key}")
    print("\n⚠️  IMPORTANT : Gardez cette clé secrète en sécurité !")

if __name__ == "__main__":
    main() 