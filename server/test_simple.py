#!/usr/bin/env python3
"""
Test simple de l'API
"""

import requests
import json

def test_simple():
    """Test simple de l'API"""
    print("=" * 40)
    print("TEST SIMPLE DE L'API")
    print("=" * 40)
    
    # URL du serveur
    base_url = "http://localhost:8000"
    
    # 1. Test de l'endpoint racine
    print("1. Test de l'endpoint racine...")
    try:
        response = requests.get(f"{base_url}/api/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API accessible")
            print(f"Réponse: {response.json()}")
        else:
            print(f"❌ Erreur: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    # 2. Test de connexion
    print("\n2. Test de connexion...")
    login_data = {
        "phone": "+22241240690",
        "password": "Moussa123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get('access')
            print("✅ Connexion réussie")
            print(f"Token: {token[:20]}...")
            return True
        else:
            print(f"❌ Erreur connexion: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_simple()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 TEST SIMPLE RÉUSSI!")
        print("✅ L'API fonctionne correctement")
    else:
        print("❌ TEST SIMPLE ÉCHOUÉ")
    print("=" * 40) 