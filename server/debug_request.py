#!/usr/bin/env python3
"""
Script pour déboguer la requête exacte
"""

import requests
import json
import os

def debug_request():
    """Déboguer la requête exacte"""
    print("=" * 50)
    print("DEBUG REQUEST")
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
        "Authorization": f"Bearer {token}"
    }
    
    # 2. Upload d'une image
    print("\n2. Upload d'une image...")
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/debug_image.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("debug_image.png", f, "image/png")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload: {upload_response.status_code}")
        print(f"Réponse upload: {upload_response.text}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            image_url = upload_data.get('url')
            print("✅ Upload image réussi!")
            print(f"URL: {image_url}")
        else:
            print(f"❌ Upload échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return False
    
    # 3. Création d'hôtel avec image
    print("\n3. Création d'hôtel avec image...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    hotel_data = {
        "name": "Hôtel Debug Test",
        "description": "Hôtel de test pour debug",
        "address": "123 Rue Debug, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "debug@hotel.com",
        "stars": 3,
        "wifi": True,
        "air_conditioning": True,
        "restaurant": False,
        "pool": False,
        "gym": False,
        "spa": False,
        "parking": True,
        "airport_shuttle": False,
        "image_urls": [image_url],
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
    success = debug_request()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 DEBUG RÉUSSI!")
    else:
        print("❌ DEBUG ÉCHOUÉ")
    print("=" * 50) 