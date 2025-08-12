#!/usr/bin/env python3
"""
Script de test pour vérifier l'upload et la création d'hôtel
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')
django.setup()

from django.conf import settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
import cloudinary

def test_upload_endpoint():
    """Test de l'endpoint d'upload"""
    print("=" * 60)
    print("TEST DE L'ENDPOINT UPLOAD")
    print("=" * 60)
    
    client = APIClient()
    
    # Créer un fichier de test
    test_content = b"Test image content"
    test_file = SimpleUploadedFile(
        "test_image.jpg",
        test_content,
        content_type="image/jpeg"
    )
    
    # Préparer les données de la requête
    data = {
        'file': test_file,
        'type': 'hotel'
    }
    
    try:
        # Faire la requête POST vers l'endpoint d'upload
        response = client.post('/api/upload/', data, format='multipart')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data}")
        
        if response.status_code == 200:
            print("✅ Upload réussi!")
            return response.data.get('url')
        else:
            print(f"❌ Erreur upload: {response.data}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors de l'upload: {e}")
        return None

def test_hotel_creation():
    """Test de la création d'hôtel"""
    print("\n" + "=" * 60)
    print("TEST DE CRÉATION D'HÔTEL")
    print("=" * 60)
    
    client = APIClient()
    
    # Données de test pour l'hôtel
    hotel_data = {
        'name': 'Hôtel Test Upload',
        'description': 'Hôtel de test pour vérifier l\'upload',
        'address': '123 Rue Test, Nouakchott',
        'city': 'Nouakchott',
        'country': 'Mauritanie',
        'phone': '+22212345678',
        'email': 'test@hotel.com',
        'stars': 3,
        'wifi': True,
        'air_conditioning': True,
        'restaurant': False,
        'pool': False,
        'gym': False,
        'spa': False,
        'parking': True,
        'airport_shuttle': False,
        'room_types': [
            {
                'name': 'Chambre Standard',
                'category': 'double',
                'description': 'Chambre confortable',
                'price_per_night': '150.00',
                'capacity': 2,
                'is_available': True
            }
        ]
    }
    
    try:
        # Faire la requête POST vers l'endpoint de création d'hôtel
        response = client.post('/api/hotels/', hotel_data, format='json')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.data}")
        
        if response.status_code == 201:
            print("✅ Création d'hôtel réussie!")
            return response.data.get('id')
        else:
            print(f"❌ Erreur création hôtel: {response.data}")
            return None
            
    except Exception as e:
        print(f"❌ Exception lors de la création: {e}")
        return None

if __name__ == "__main__":
    print("Démarrage des tests d'upload et création d'hôtel...")
    
    # Test d'upload
    upload_url = test_upload_endpoint()
    
    # Test de création d'hôtel
    hotel_id = test_hotel_creation()
    
    print("\n" + "=" * 60)
    if upload_url and hotel_id:
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print(f"✅ Upload URL: {upload_url}")
        print(f"✅ Hôtel créé avec ID: {hotel_id}")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print("=" * 60) 