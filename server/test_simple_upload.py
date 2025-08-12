#!/usr/bin/env python3
"""
Test simple de l'upload
"""

import requests
import json
import os

def test_simple_upload():
    """Test simple de l'upload"""
    print("=" * 50)
    print("TEST SIMPLE UPLOAD")
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
    
    # 2. Créer une image PNG valide
    print("\n2. Création d'une image de test...")
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_simple.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    print("✅ Image de test créée")
    
    # 3. Test d'upload
    print("\n3. Test d'upload d'image...")
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_simple.png", f, "image/png")}
            data = {"type": "hotel"}
            
            upload_response = requests.post(
                f"{base_url}/api/upload/",
                files=files,
                data=data,
                headers=headers
            )
        
        print(f"Status upload: {upload_response.status_code}")
        print(f"Réponse: {upload_response.text}")
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            if 'url' in upload_data:
                image_url = upload_data.get('url')
                print("✅ Upload image réussi!")
                print(f"URL: {image_url}")
                return True
            else:
                print("❌ Pas d'URL dans la réponse")
                return False
        else:
            print(f"❌ Upload échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_upload()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST RÉUSSI!")
        print("✅ Upload d'images fonctionne")
    else:
        print("❌ TEST ÉCHOUÉ")
    print("=" * 50) 