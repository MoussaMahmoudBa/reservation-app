#!/usr/bin/env python3
"""
Test de l'état d'authentification
"""

import requests
import json

def test_auth_status():
    """Test de l'état d'authentification"""
    print("=" * 50)
    print("TEST ÉTAT D'AUTHENTIFICATION")
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
            user_data = token_data.get('user', {})
            print("✅ Connexion réussie")
            print(f"Access token: {access_token[:20]}...")
            print(f"User data: {json.dumps(user_data, indent=2)}")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. Test du profil utilisateur
    print("\n2. Test du profil utilisateur...")
    
    try:
        profile_response = requests.get(f"{base_url}/api/auth/profile/", headers=headers)
        print(f"Status profile: {profile_response.status_code}")
        print(f"Réponse profile: {profile_response.text}")
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print("✅ Profil utilisateur accessible!")
            print(f"Données profil: {json.dumps(profile_data, indent=2)}")
        else:
            print(f"❌ Erreur profil: {profile_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur profil: {e}")
        return False
    
    # 3. Test d'accès aux hôtels (admin)
    print("\n3. Test d'accès aux hôtels (admin)...")
    
    try:
        hotels_response = requests.get(f"{base_url}/api/hotels/", headers=headers)
        print(f"Status hotels: {hotels_response.status_code}")
        
        if hotels_response.status_code == 200:
            print("✅ Accès aux hôtels autorisé!")
        else:
            print(f"❌ Erreur accès hôtels: {hotels_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur accès hôtels: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TEST AUTH RÉUSSI!")
    print("✅ Connexion fonctionne")
    print("✅ Profil utilisateur accessible")
    print("✅ Accès admin autorisé")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = test_auth_status()
    
    if not success:
        print("\n❌ TEST AUTH ÉCHOUÉ")
        print("⚠️  Problème d'authentification détecté") 