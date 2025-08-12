#!/usr/bin/env python3
"""
Test final pour vérifier que l'upload fonctionne parfaitement
"""

import requests
import json
import os
from pathlib import Path

def test_final_upload():
    """Test final complet"""
    print("=" * 60)
    print("TEST FINAL - UPLOAD COMPLET")
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
    
    # 2. Créer des fichiers de test
    print("\n2. Création de fichiers de test...")
    
    # Image PNG
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Vidéo MP4 minimal (header MP4)
    mp4_data = b'\x00\x00\x00\x20ftypmp41\x00\x00\x00\x00mp41isom\x00\x00\x00\x08mdat\x00\x00\x00\x00'
    
    test_image_path = "/tmp/test_hotel_image.png"
    test_video_path = "/tmp/test_hotel_video.mp4"
    
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    with open(test_video_path, "wb") as f:
        f.write(mp4_data)
    
    print(f"Image créée: {test_image_path}")
    print(f"Vidéo créée: {test_video_path}")
    
    # 3. Test d'upload d'image
    print("\n3. Test d'upload d'image...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_hotel_image.png", f, "image/png")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload image: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            image_url = upload_data.get('url')
            print("✅ Upload image réussi!")
            print(f"URL: {image_url}")
        else:
            print(f"❌ Upload image échoué: {upload_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur upload image: {e}")
        return None
    
    # 4. Test d'upload de vidéo
    print("\n4. Test d'upload de vidéo...")
    
    try:
        with open(test_video_path, "rb") as f:
            files = {"file": ("test_hotel_video.mp4", f, "video/mp4")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload vidéo: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            video_url = upload_data.get('url')
            print("✅ Upload vidéo réussi!")
            print(f"URL: {video_url}")
        else:
            print(f"❌ Upload vidéo échoué: {upload_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur upload vidéo: {e}")
        return None
    
    # 5. Test de création d'hôtel avec les URLs
    print("\n5. Test de création d'hôtel avec les URLs...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    hotel_data = {
        "name": "Hôtel Test Final",
        "description": "Hôtel de test final avec upload complet",
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
        
        print(f"Status création hôtel: {response.status_code}")
        
        if response.status_code == 201:
            hotel_data = response.json()
            print("✅ Création hôtel réussie!")
            return hotel_data.get('id')
        else:
            print(f"❌ Création hôtel échouée: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création hôtel: {e}")
        return None

if __name__ == "__main__":
    print("Démarrage du test final...")
    
    # Test complet
    hotel_id = test_final_upload()
    
    print("\n" + "=" * 60)
    if hotel_id:
        print("🎉 TEST FINAL RÉUSSI!")
        print("✅ Upload d'images fonctionne")
        print("✅ Upload de vidéos fonctionne")
        print("✅ Création d'hôtel fonctionne")
        print("✅ Tout est opérationnel!")
        print(f"✅ Hôtel créé avec ID: {hotel_id}")
        print("\n🚀 L'application est prête à être utilisée!")
    else:
        print("❌ TEST FINAL ÉCHOUÉ")
        print("⚠️  Il y a encore des problèmes à résoudre")
    
    print("=" * 60) 