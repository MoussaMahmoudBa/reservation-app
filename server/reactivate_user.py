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
print("RÉACTIVATION DE L'UTILISATEUR")
print("=" * 60)

try:
    # Trouver l'utilisateur (ID: 9)
    user = User.objects.get(id=9)
    
    print(f"Utilisateur trouvé: {user.get_full_name()}")
    print(f"Statut actuel: {'Actif' if user.is_active else 'Inactif'}")
    print("Réactivation en cours...")
    
    # Remettre l'utilisateur en actif
    user.is_active = True
    user.save()
    
    print("✅ Utilisateur réactivé avec succès!")
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
    print(f"❌ Erreur lors de la réactivation: {e}") 