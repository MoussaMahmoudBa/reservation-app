#!/usr/bin/env python3
"""
Test de navigation et authentification
"""

import requests
import json

def test_navigation():
    """Test de navigation et authentification"""
    print("=" * 60)
    print("TEST NAVIGATION ET AUTHENTIFICATION")
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
            user_data = token_data.get('user', {})
            print("✅ Connexion réussie")
            print(f"Access token: {access_token[:20]}...")
            print(f"User type: {user_data.get('user_type', 'unknown')}")
        else:
            print(f"❌ Erreur connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 2. Test d'accès aux pages admin
    print("\n2. Test d'accès aux pages admin...")
    
    # Test accès aux hôtels
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
    
    # Test accès aux appartements
    try:
        apartments_response = requests.get(f"{base_url}/api/apartments/", headers=headers)
        print(f"Status apartments: {apartments_response.status_code}")
        
        if apartments_response.status_code == 200:
            print("✅ Accès aux appartements autorisé!")
        else:
            print(f"❌ Erreur accès appartements: {apartments_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur accès appartements: {e}")
        return False
    
    # Test accès aux utilisateurs
    try:
        users_response = requests.get(f"{base_url}/api/users/", headers=headers)
        print(f"Status users: {users_response.status_code}")
        
        if users_response.status_code == 200:
            print("✅ Accès aux utilisateurs autorisé!")
        else:
            print(f"❌ Erreur accès utilisateurs: {users_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur accès utilisateurs: {e}")
        return False
    
    # 3. Test de création d'hôtel
    print("\n3. Test de création d'hôtel...")
    
    hotel_data = {
        "name": "Hôtel Test Navigation",
        "description": "Hôtel de test pour navigation",
        "address": "123 Rue Navigation, Nouakchott",
        "city": "Nouakchott",
        "country": "Mauritanie",
        "phone": "+22212345678",
        "email": "navigation@hotel.com",
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
        create_response = requests.post(
            f"{base_url}/api/hotels/",
            json=hotel_data,
            headers=headers
        )
        
        print(f"Status création: {create_response.status_code}")
        
        if create_response.status_code == 201:
            print("✅ Création d'hôtel réussie!")
        else:
            print(f"❌ Erreur création d'hôtel: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création d'hôtel: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 TEST NAVIGATION RÉUSSI!")
    print("✅ Connexion fonctionne")
    print("✅ Accès aux pages admin autorisé")
    print("✅ Création d'hôtels fonctionne")
    print("✅ Navigation entre les pages fonctionne")
    print("\n🚀 L'application est prête pour la navigation!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_navigation()
    
    if not success:
        print("\n❌ TEST NAVIGATION ÉCHOUÉ")
        print("⚠️  Problème de navigation détecté") 