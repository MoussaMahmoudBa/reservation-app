#!/usr/bin/env python3
"""
Script pour créer un utilisateur admin
"""

import os
import sys
import django

# Ajouter le répertoire server au path
sys.path.append('/home/moussa-ba/Bureau/Reservation/server')

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')
django.setup()

from users.models import User

def create_admin_user():
    """Créer un utilisateur admin"""
    
    print("🔧 Création d'un utilisateur admin...")
    
    # Vérifier si l'admin existe déjà
    admin_phone = "+22212345678"
    admin_email = "admin@example.com"
    
    try:
        existing_admin = User.objects.get(phone=admin_phone)
        print(f"✅ L'admin existe déjà: {existing_admin.username}")
        print(f"   Email: {existing_admin.email}")
        print(f"   Téléphone: {existing_admin.phone}")
        print(f"   Type: {existing_admin.user_type}")
        return existing_admin
    except User.DoesNotExist:
        pass
    
    # Créer l'admin
    try:
        admin_user = User.objects.create_user(
            username="admin",
            email=admin_email,
            phone=admin_phone,
            password="admin123",
            first_name="Admin",
            last_name="User",
            user_type="admin",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_verified=True
        )
        
        print("✅ Utilisateur admin créé avec succès!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Téléphone: {admin_user.phone}")
        print(f"   Type: {admin_user.user_type}")
        print(f"   Mot de passe: admin123")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        admin = create_admin_user()
        if admin:
            print("\n🎉 Admin créé/prêt!")
        else:
            print("\n❌ Échec de la création de l'admin")
    except Exception as e:
        print(f"\n💥 Erreur: {str(e)}")
        import traceback
        traceback.print_exc() 