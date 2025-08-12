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
print("VÉRIFICATION DES UTILISATEURS DANS POSTGRESQL")
print("=" * 60)

try:
    # Compter les utilisateurs
    total = User.objects.count()
    print(f"Nombre total d'utilisateurs: {total}")
    
    if total == 0:
        print("Aucun utilisateur trouvé dans la base de données PostgreSQL.")
    else:
        print("\nListe des utilisateurs:")
        print("-" * 50)
        
        for user in User.objects.all().order_by('-created_at'):
            print(f"ID: {user.id}")
            print(f"Nom d'utilisateur: {user.username}")
            print(f"Nom complet: {user.get_full_name()}")
            print(f"Téléphone: {user.phone}")
            print(f"Email: {user.email or 'Non renseigné'}")
            print(f"Type: {user.get_user_type_display()}")
            print(f"Vérifié: {'Oui' if user.is_verified else 'Non'}")
            print(f"Actif: {'Oui' if user.is_active else 'Non'}")
            print(f"Superuser: {'Oui' if user.is_superuser else 'Non'}")
            print(f"Date de création: {user.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
            if user.address:
                print(f"Adresse: {user.address}")
            print("-" * 30)
            
        # Statistiques
        print("\n" + "=" * 40)
        print("STATISTIQUES")
        print("=" * 40)
        clients = User.objects.filter(user_type='client').count()
        admins = User.objects.filter(user_type='admin').count()
        superusers = User.objects.filter(is_superuser=True).count()
        verified = User.objects.filter(is_verified=True).count()
        active = User.objects.filter(is_active=True).count()
        
        print(f"Total: {total}")
        print(f"Clients: {clients}")
        print(f"Administrateurs: {admins}")
        print(f"Superusers: {superusers}")
        print(f"Vérifiés: {verified}")
        print(f"Actifs: {active}")
            
except Exception as e:
    print(f"Erreur de connexion à PostgreSQL: {e}")
    print("Vérifiez que PostgreSQL est en cours d'exécution sur le port 5433") 