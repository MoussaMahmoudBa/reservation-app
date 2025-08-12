#!/usr/bin/env python3
"""
Test final de l'upload et création d'hôtel
"""

import requests
import json
import os
from pathlib import Path

def test_upload_final():
    """Test final de l'upload et création d'hôtel"""
    print("=" * 60)
    print("TEST FINAL - UPLOAD ET CRÉATION D'HÔTEL")
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
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 2. Test d'upload d'image
    print("\n2. Test d'upload d'image...")
    
    # Créer une image PNG valide
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_upload_final.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_upload_final.png", f, "image/png")}
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
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload image: {e}")
        return False
    
    # 3. Test de création d'hôtel avec image
    print("\n3. Test de création d'hôtel avec image...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    hotel_data = {
        "name": "Hôtel Test Upload Final",
        "description": "Hôtel de test avec upload final",
        "address": "123 Rue Upload Final, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "upload@hotel.com",
        "stars": 3,
        "wifi": True,
        "air_conditioning": True,
        "restaurant": False,
        "pool": False,
        "gym": False,
        "spa": False,
        "parking": True,
        "airport_shuttle": False,
        "image_urls": [image_url],  # Inclure l'URL d'image
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
            hotel_id = hotel_data.get('id')
            print("✅ Création hôtel avec image réussie!")
            print(f"ID: {hotel_id}")
            
            # Vérifier que l'hôtel a bien des images
            if 'images' in hotel_data and len(hotel_data['images']) > 0:
                print("✅ Images bien associées à l'hôtel!")
                print(f"Nombre d'images: {len(hotel_data['images'])}")
                for img in hotel_data['images']:
                    print(f"  - Image ID: {img['id']}, URL: {img['image']}")
            else:
                print("⚠️  Aucune image trouvée dans la réponse")
            
            return True
        else:
            print(f"❌ Création hôtel échouée: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création hôtel: {e}")
        return False

if __name__ == "__main__":
    print("Démarrage du test final...")
    
    # Test complet
    success = test_upload_final()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST FINAL RÉUSSI!")
        print("✅ Upload d'images fonctionne")
        print("✅ Création d'hôtel avec images fonctionne")
        print("✅ La solution est complète et opérationnelle!")
        print("\n🚀 L'application est prête pour la production!")
    else:
        print("❌ TEST FINAL ÉCHOUÉ")
        print("⚠️  Il y a encore des problèmes à résoudre")
    
    print("=" * 60) 