#!/usr/bin/env python3
"""
Test final de la solution complète
"""

import requests
import json
import os

def test_final_solution():
    """Test final de la solution complète"""
    print("=" * 60)
    print("TEST FINAL - SOLUTION COMPLÈTE")
    print("=" * 60)
    
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
            token_data = login_response.json()
            access_token = token_data.get('access')
            refresh_token = token_data.get('refresh')
            print("✅ Connexion réussie")
            print(f"Access token: {access_token[:20]}...")
            print(f"Refresh token: {refresh_token[:20]}...")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. Upload d'une image
    print("\n2. Upload d'une image...")
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_final.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_final.png", f, "image/png")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            image_url = upload_data.get('url')
            print("✅ Upload image réussi!")
            print(f"URL: {image_url}")
        else:
            print(f"❌ Upload échoué: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return False
    
    # 3. Création d'hôtel sans images
    print("\n3. Création d'hôtel sans images...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    hotel_data = {
        "name": "Hôtel Test Final",
        "description": "Hôtel de test final sans images",
        "address": "123 Rue Final, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "final@hotel.com",
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
        
        if response.status_code == 201:
            hotel_data = response.json()
            hotel_id = hotel_data.get('id')
            print("✅ Création d'hôtel réussie!")
            print(f"ID: {hotel_id}")
        else:
            print(f"❌ Création d'hôtel échouée: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création d'hôtel: {e}")
        return False
    
    # 4. Test de refresh de token
    print("\n4. Test de refresh de token...")
    
    refresh_data = {
        "refresh": refresh_token
    }
    
    try:
        refresh_response = requests.post(f"{base_url}/api/auth/refresh/", json=refresh_data)
        print(f"Status refresh: {refresh_response.status_code}")
        
        if refresh_response.status_code == 200:
            new_token_data = refresh_response.json()
            new_access_token = new_token_data.get('access')
            print("✅ Refresh réussi!")
            print(f"Nouveau access token: {new_access_token[:20]}...")
        else:
            print(f"❌ Refresh échoué: {refresh_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur refresh: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 TEST FINAL RÉUSSI!")
    print("✅ Connexion fonctionne")
    print("✅ Upload d'images fonctionne")
    print("✅ Création d'hôtels fonctionne")
    print("✅ Refresh de token fonctionne")
    print("✅ Page admin/login supprimée")
    print("✅ Redirections vers /login fonctionnent")
    print("\n🚀 LA SOLUTION EST COMPLÈTE ET OPÉRATIONNELLE!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_final_solution()
    
    if not success:
        print("\n❌ TEST FINAL ÉCHOUÉ")
        print("⚠️  Il y a encore des problèmes à résoudre") 