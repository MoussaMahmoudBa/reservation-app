#!/usr/bin/env python3
"""
Test final confirmant que l'upload d'images fonctionne
"""

import requests
import json
import os
from pathlib import Path

def test_image_upload_success():
    """Test confirmant que l'upload d'images fonctionne"""
    print("=" * 60)
    print("TEST FINAL - UPLOAD D'IMAGES FONCTIONNEL")
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
    
    # Créer une image PNG valide (1x1 pixel transparent)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_success_image.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_success_image.png", f, "image/png")}
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
            return True
        else:
            print(f"❌ Upload image échoué: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload image: {e}")
        return False

def test_apartment_image_upload():
    """Test d'upload d'image pour appartement"""
    print("\n3. Test d'upload d'image pour appartement...")
    
    # URL du serveur
    base_url = "http://localhost:8000"
    
    # Se connecter
    login_data = {
        "phone": "+22241240690",
        "password": "Moussa123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('access')
        else:
            print("❌ Erreur connexion pour test appartement")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion pour test appartement: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer une image PNG valide
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_apartment_image.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_apartment_image.png", f, "image/png")}
            data = {"type": "apartment"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload image appartement: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            image_url = upload_data.get('url')
            print("✅ Upload image appartement réussi!")
            print(f"URL: {image_url}")
            return True
        else:
            print(f"❌ Upload image appartement échoué: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload image appartement: {e}")
        return False

if __name__ == "__main__":
    print("Démarrage du test final d'upload...")
    
    # Test upload d'images pour hôtels
    hotel_success = test_image_upload_success()
    
    # Test upload d'images pour appartements
    apartment_success = test_apartment_image_upload()
    
    print("\n" + "=" * 60)
    if hotel_success and apartment_success:
        print("🎉 SUCCÈS COMPLET!")
        print("✅ Upload d'images pour hôtels fonctionne")
        print("✅ Upload d'images pour appartements fonctionne")
        print("✅ L'application est opérationnelle!")
        print("\n🚀 L'upload d'images est prêt à être utilisé dans l'interface admin!")
        print("\n📝 Note sur les vidéos:")
        print("   - L'upload de vidéos nécessite des fichiers vidéo réels")
        print("   - Les fichiers de test minimalistes sont rejetés par Cloudinary")
        print("   - Pour tester les vidéos, utilisez de vrais fichiers MP4/MOV")
        print("\n✨ Le problème d'upload d'images est RÉSOLU!")
    elif hotel_success:
        print("✅ Upload d'images pour hôtels fonctionne")
        print("⚠️  Upload d'images pour appartements à vérifier")
    elif apartment_success:
        print("✅ Upload d'images pour appartements fonctionne")
        print("⚠️  Upload d'images pour hôtels à vérifier")
    else:
        print("❌ PROBLÈME PERSISTANT")
        print("⚠️  L'upload d'images ne fonctionne pas")
    
    print("=" * 60) 