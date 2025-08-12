#!/usr/bin/env python3
"""
Test de validité du token
"""

import requests
import json

def test_token():
    """Test de validité du token"""
    print("=" * 50)
    print("TEST DE VALIDITÉ DU TOKEN")
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
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    # 2. Test d'upload avec token
    print("\n2. Test d'upload avec token...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Créer une image de test
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xf7\xa0\xc8\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image_path = "/tmp/test_token.png"
    with open(test_image_path, "wb") as f:
        f.write(png_data)
    
    try:
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_token.png", f, "image/png")}
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
            print("✅ Upload réussi avec token valide!")
            return True
        else:
            print(f"❌ Upload échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return False

if __name__ == "__main__":
    success = test_token()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TOKEN VALIDE!")
        print("✅ L'authentification fonctionne")
    else:
        print("❌ PROBLÈME AVEC LE TOKEN")
    print("=" * 50) 