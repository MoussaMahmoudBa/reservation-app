#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')
django.setup()

from users.models import User

def list_users():
    """Affiche tous les utilisateurs dans la base de données"""
    print("=" * 80)
    print("LISTE DES UTILISATEURS DANS LA BASE DE DONNÉES")
    print("=" * 80)
    
    users = User.objects.all().order_by('-created_at')
    
    if not users.exists():
        print("Aucun utilisateur trouvé dans la base de données.")
        return
    
    print(f"Nombre total d'utilisateurs: {users.count()}")
    print()
    
    for i, user in enumerate(users, 1):
        print(f"Utilisateur #{i}")
        print(f"  ID: {user.id}")
        print(f"  Nom d'utilisateur: {user.username}")
        print(f"  Nom complet: {user.get_full_name()}")
        print(f"  Téléphone: {user.phone}")
        print(f"  Email: {user.email or 'Non renseigné'}")
        print(f"  Type: {user.get_user_type_display()}")
        print(f"  Vérifié: {'Oui' if user.is_verified else 'Non'}")
        print(f"  Superuser: {'Oui' if user.is_superuser else 'Non'}")
        print(f"  Actif: {'Oui' if user.is_active else 'Non'}")
        print(f"  Date de création: {user.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        if user.date_of_birth:
            print(f"  Date de naissance: {user.date_of_birth.strftime('%d/%m/%Y')}")
        if user.address:
            print(f"  Adresse: {user.address}")
        print("-" * 40)

def list_users_summary():
    """Affiche un résumé des utilisateurs"""
    print("=" * 50)
    print("RÉSUMÉ DES UTILISATEURS")
    print("=" * 50)
    
    total_users = User.objects.count()
    clients = User.objects.filter(user_type='client').count()
    admins = User.objects.filter(user_type='admin').count()
    superusers = User.objects.filter(is_superuser=True).count()
    verified_users = User.objects.filter(is_verified=True).count()
    active_users = User.objects.filter(is_active=True).count()
    
    print(f"Total utilisateurs: {total_users}")
    print(f"  - Clients: {clients}")
    print(f"  - Administrateurs: {admins}")
    print(f"  - Superusers: {superusers}")
    print(f"  - Vérifiés: {verified_users}")
    print(f"  - Actifs: {active_users}")

if __name__ == "__main__":
    try:
        list_users_summary()
        print()
        list_users()
    except Exception as e:
        print(f"Erreur lors de l'interrogation de la base de données: {e}")
        sys.exit(1) 