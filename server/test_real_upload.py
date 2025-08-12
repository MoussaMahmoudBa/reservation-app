#!/usr/bin/env python3
"""
Script de test pour l'upload avec le serveur réel
"""

import requests
import json
import os
from pathlib import Path

def test_real_upload():
    """Test d'upload avec le serveur réel"""
    print("=" * 60)
    print("TEST UPLOAD AVEC SERVEUR RÉEL")
    print("=" * 60)
    
    # URL du serveur
    base_url = "http://localhost:8000"
    
    # 1. Se connecter pour obtenir un token
    print("1. Connexion...")
    login_data = {
        "phone": "+22241240690",
        "password": "Moussa123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        print(f"Status login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('access')
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return None
    
    # 2. Test d'upload
    print("\n2. Test d'upload...")
    
    # Créer une vraie image PNG de test
    test_file_path = "/tmp/test_image.png"
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    with open(test_file_path, "wb") as f:
        f.write(png_data)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_image.png", f, "image/png")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload: {upload_response.status_code}")
        print(f"Response: {upload_response.text}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            print("✅ Upload réussi!")
            return upload_data.get('url'), token
        else:
            print("❌ Upload échoué!")
            return None, token
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return None, token

def test_real_hotel_creation(upload_url, token):
    """Test de création d'hôtel avec le serveur réel"""
    print("\n" + "=" * 60)
    print("TEST CRÉATION HÔTEL AVEC SERVEUR RÉEL")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    hotel_data = {
        "name": "Hôtel Test Réel",
        "description": "Hôtel de test avec upload réel",
        "address": "123 Rue Test, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "test@hotel.com",
        "stars": 3,
        "wifi": True,
        "air_conditioning": True,
        "restaurant": False,
        "pool": False,
        "gym": False,
        "spa": False,
        "parking": True,
        "airport_shuttle": False,
        "room_types": [
            {
                "name": "Chambre Standard",
                "category": "double",
                "description": "Chambre confortable",
                "price_per_night": "150.00",
                "capacity": 2,
                "is_available": True
            }
        ]
    }
    
    print(f"Données envoyées: {json.dumps(hotel_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/api/hotels/",
            json=hotel_data,
            headers=headers
        )
        
        print(f"Status création: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            hotel_data = response.json()
            print("✅ Création hôtel réussie!")
            return hotel_data.get('id')
        else:
            print("❌ Création hôtel échouée!")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création: {e}")
        return None

if __name__ == "__main__":
    print("Démarrage des tests avec serveur réel...")
    
    # Test d'upload
    upload_url, token = test_real_upload()
    
    if upload_url and token:
        # Test de création d'hôtel
        hotel_id = test_real_hotel_creation(upload_url, token)
        
        print("\n" + "=" * 60)
        if hotel_id:
            print("🎉 TOUS LES TESTS SONT PASSÉS!")
            print(f"✅ Upload URL: {upload_url}")
            print(f"✅ Hôtel créé avec ID: {hotel_id}")
        else:
            print("⚠️  Upload OK mais création hôtel échouée")
    else:
        print("\n❌ TESTS ÉCHOUÉS")
    
    print("=" * 60) 