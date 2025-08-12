#!/usr/bin/env python3
"""
Test simple de création d'hôtel sans images
"""

import requests
import json

def test_simple_creation():
    """Test simple de création d'hôtel sans images"""
    print("=" * 50)
    print("TEST CRÉATION SIMPLE SANS IMAGES")
    print("=" * 50)
    
    # URL du serveur
    base_url = "http://localhost:8000"
    
    # 1. Se connecter
    print("1. Connexion...")
    login_data = {
        "phone": "+22241240690",
        "password": "Moussa123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        print(f"Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('access')
            print("✅ Connexion réussie")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Création d'hôtel sans images
    print("\n2. Création d'hôtel sans images...")
    
    hotel_data = {
        "name": "Hôtel Test Simple",
        "description": "Hôtel de test simple sans images",
        "address": "123 Rue Simple, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "simple@hotel.com",
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
    
    try:
        response = requests.post(
            f"{base_url}/api/hotels/",
            json=hotel_data,
            headers=headers
        )
        
        print(f"Status création: {response.status_code}")
        print(f"Réponse création: {response.text}")
        
        if response.status_code == 201:
            hotel_data = response.json()
            hotel_id = hotel_data.get('id')
            print("✅ Création d'hôtel réussie!")
            print(f"ID: {hotel_id}")
            return True
        else:
            print(f"❌ Création d'hôtel échouée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création d'hôtel: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST RÉUSSI!")
        print("✅ Création d'hôtel sans images fonctionne")
        print("✅ Le problème principal est résolu!")
    else:
        print("❌ TEST ÉCHOUÉ")
    print("=" * 50) 