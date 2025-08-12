#!/usr/bin/env python3
"""
Script de debug pour analyser les problèmes d'upload et de création d'hôtel
"""

import os
import sys
import django
from pathlib import Path
import json

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_project.settings')
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
import cloudinary

def debug_cloudinary_config():
    """Debug de la configuration Cloudinary"""
    print("=" * 60)
    print("DEBUG CONFIGURATION CLOUDINARY")
    print("=" * 60)
    
    cloud_name = settings.CLOUDINARY.get('cloud_name')
    api_key = settings.CLOUDINARY.get('api_key')
    api_secret = settings.CLOUDINARY.get('api_secret')
    
    print(f"Cloud Name: {cloud_name}")
    print(f"API Key: {api_key}")
    print(f"API Secret: {'*' * len(api_secret) if api_secret else 'Non configuré'}")
    
    if not all([cloud_name, api_key, api_secret]):
        print("❌ Configuration Cloudinary incomplète!")
        return False
    
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print("✅ Configuration Cloudinary OK")
        return True
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def debug_upload_with_details():
    """Debug détaillé de l'upload"""
    print("\n" + "=" * 60)
    print("DEBUG UPLOAD DÉTAILLÉ")
    print("=" * 60)
    
    client = APIClient()
    
    # Créer un fichier de test plus réaliste
    test_content = b"Fake JPEG content for testing"
    test_file = SimpleUploadedFile(
        "test_hotel_image.jpg",
        test_content,
        content_type="image/jpeg"
    )
    
    data = {
        'file': test_file,
        'type': 'hotel'
    }
    
    print(f"Fichier créé: {test_file.name}")
    print(f"Taille: {len(test_content)} bytes")
    print(f"Type MIME: {test_file.content_type}")
    
    try:
        response = client.post('/api/upload/', data, format='multipart')
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if hasattr(response, 'data'):
            print(f"Response Data: {json.dumps(response.data, indent=2)}")
        else:
            print(f"Response Content: {response.content.decode()}")
        
        if response.status_code == 200:
            print("✅ Upload réussi!")
            return response.data.get('url') if hasattr(response, 'data') else None
        else:
            print("❌ Upload échoué!")
            return None
            
    except Exception as e:
        print(f"❌ Exception upload: {e}")
        import traceback
        traceback.print_exc()
        return None

def debug_hotel_creation_with_details():
    """Debug détaillé de la création d'hôtel"""
    print("\n" + "=" * 60)
    print("DEBUG CRÉATION HÔTEL DÉTAILLÉ")
    print("=" * 60)
    
    client = APIClient()
    
    # Données de test minimales
    hotel_data = {
        'name': 'Hôtel Debug Test',
        'description': 'Hôtel de test pour debug',
        'address': '123 Rue Debug, Nouakchott',
        'city': 'Nouakchott',
        'country': 'Mauritanie',
        'phone': '+22212345678',
        'email': 'debug@hotel.com',
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
    
    print(f"Données envoyées: {json.dumps(hotel_data, indent=2)}")
    
    try:
        response = client.post('/api/hotels/', hotel_data, format='json')
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if hasattr(response, 'data'):
            print(f"Response Data: {json.dumps(response.data, indent=2)}")
        else:
            print(f"Response Content: {response.content.decode()}")
        
        if response.status_code == 201:
            print("✅ Création hôtel réussie!")
            return response.data.get('id') if hasattr(response, 'data') else None
        else:
            print("❌ Création hôtel échouée!")
            return None
            
    except Exception as e:
        print(f"❌ Exception création: {e}")
        import traceback
        traceback.print_exc()
        return None

def debug_serializer_validation():
    """Debug de la validation du sérialiseur"""
    print("\n" + "=" * 60)
    print("DEBUG VALIDATION SÉRIALISEUR")
    print("=" * 60)
    
    from hotels.serializers import HotelCreateSerializer
    from hotels.models import Hotel
    
    # Données de test
    data = {
        'name': 'Hôtel Test Validation',
        'description': 'Test validation',
        'address': '123 Test',
        'city': 'Nouakchott',
        'country': 'Mauritanie',
        'phone': '+22212345678',
        'email': 'test@hotel.com',
        'stars': 3,
        'room_types': [
            {
                'name': 'Chambre Test',
                'category': 'double',
                'description': 'Test',
                'price_per_night': '100.00',
                'capacity': 2,
                'is_available': True
            }
        ]
    }
    
    print(f"Données à valider: {json.dumps(data, indent=2)}")
    
    serializer = HotelCreateSerializer(data=data)
    
    if serializer.is_valid():
        print("✅ Validation sérialiseur OK")
        print(f"Données validées: {serializer.validated_data}")
        return True
    else:
        print("❌ Erreurs de validation:")
        print(json.dumps(serializer.errors, indent=2))
        return False

if __name__ == "__main__":
    print("Démarrage du debug complet...")
    
    # Debug configuration
    config_ok = debug_cloudinary_config()
    
    if config_ok:
        # Debug upload
        upload_url = debug_upload_with_details()
        
        # Debug création hôtel
        hotel_id = debug_hotel_creation_with_details()
        
        # Debug validation sérialiseur
        validation_ok = debug_serializer_validation()
        
        print("\n" + "=" * 60)
        print("RÉSUMÉ DU DEBUG")
        print("=" * 60)
        print(f"Configuration Cloudinary: {'✅' if config_ok else '❌'}")
        print(f"Upload: {'✅' if upload_url else '❌'}")
        print(f"Création hôtel: {'✅' if hotel_id else '❌'}")
        print(f"Validation sérialiseur: {'✅' if validation_ok else '❌'}")
        
        if all([config_ok, upload_url, hotel_id, validation_ok]):
            print("\n🎉 TOUT FONCTIONNE CORRECTEMENT!")
        else:
            print("\n⚠️  CERTAINS PROBLÈMES ONT ÉTÉ IDENTIFIÉS")
    else:
        print("\n❌ CONFIGURATION CLOUDINARY PROBLÉMATIQUE") 