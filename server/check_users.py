#!/usr/bin/env python
import os
import django

# Forcer SQLite
os.environ['DB_ENGINE'] = 'sqlite'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')

django.setup()

from users.models import User

print("=" * 60)
print("VÉRIFICATION DES UTILISATEURS DANS LA BASE DE DONNÉES")
print("=" * 60)

try:
    # Compter les utilisateurs
    total = User.objects.count()
    print(f"Nombre total d'utilisateurs: {total}")
    
    if total == 0:
        print("Aucun utilisateur trouvé dans la base de données.")
    else:
        print("\nListe des utilisateurs:")
        print("-" * 40)
        
        for user in User.objects.all():
            print(f"ID: {user.id}")
            print(f"Nom: {user.get_full_name()}")
            print(f"Téléphone: {user.phone}")
            print(f"Email: {user.email or 'Non renseigné'}")
            print(f"Type: {user.get_user_type_display()}")
            print(f"Actif: {'Oui' if user.is_active else 'Non'}")
            print(f"Superuser: {'Oui' if user.is_superuser else 'Non'}")
            print("-" * 20)
            
except Exception as e:
    print(f"Erreur: {e}") 