#!/usr/bin/env python
import os
import django

# Configuration PostgreSQL
os.environ['DB_ENGINE'] = 'postgres'
os.environ['DB_NAME'] = 'reservation_db'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'Moussa123'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5433'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')

django.setup()

from users.models import User

print("=" * 60)
print("MISE À JOUR DE L'UTILISATEUR")
print("=" * 60)

try:
    # Trouver l'utilisateur existant (ID: 9)
    user = User.objects.get(id=9)
    
    print(f"Utilisateur trouvé: {user.get_full_name()}")
    print("Mise à jour en cours...")
    
    # Mettre à jour les informations
    user.username = "MoussaAdmin"
    user.first_name = "Moussa"
    user.last_name = "Ba"
    user.is_verified = True
    
    # Sauvegarder les modifications
    user.save()
    
    print("✅ Mise à jour réussie!")
    print("\nNouvelles informations:")
    print("-" * 30)
    print(f"ID: {user.id}")
    print(f"Nom d'utilisateur: {user.username}")
    print(f"Nom complet: {user.get_full_name()}")
    print(f"Téléphone: {user.phone}")
    print(f"Email: {user.email}")
    print(f"Type: {user.get_user_type_display()}")
    print(f"Vérifié: {'Oui' if user.is_verified else 'Non'}")
    print(f"Actif: {'Oui' if user.is_active else 'Non'}")
    print(f"Superuser: {'Oui' if user.is_superuser else 'Non'}")
    
except User.DoesNotExist:
    print("❌ Utilisateur avec l'ID 9 non trouvé")
except Exception as e:
    print(f"❌ Erreur lors de la mise à jour: {e}") 