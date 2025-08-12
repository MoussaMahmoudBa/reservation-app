#!/usr/bin/env python3
"""
Test de refresh de token
"""

import requests
import json

def test_refresh():
    """Test de refresh de token"""
    print("=" * 50)
    print("TEST DE REFRESH DE TOKEN")
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
    
    # 2. Test de refresh
    print("\n2. Test de refresh...")
    
    refresh_data = {
        "refresh": refresh_token
    }
    
    try:
        refresh_response = requests.post(f"{base_url}/api/auth/refresh/", json=refresh_data)
        print(f"Status refresh: {refresh_response.status_code}")
        print(f"Réponse refresh: {refresh_response.text}")
        
        if refresh_response.status_code == 200:
            new_token_data = refresh_response.json()
            new_access_token = new_token_data.get('access')
            print("✅ Refresh réussi!")
            print(f"Nouveau access token: {new_access_token[:20]}...")
            return True
        else:
            print(f"❌ Refresh échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur refresh: {e}")
        return False

if __name__ == "__main__":
    success = test_refresh()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 REFRESH FONCTIONNE!")
        print("✅ Le système de refresh est opérationnel")
    else:
        print("❌ PROBLÈME AVEC LE REFRESH")
    print("=" * 50) 