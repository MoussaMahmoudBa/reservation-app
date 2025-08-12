"""
URL configuration for reservation_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import password_reset_request, password_reset_confirm, password_reset_verify
from hotels import views as hotel_views
from reservations import views as reservation_views

def api_root(request):
    """Vue de base pour l'API"""
    return JsonResponse({
        'message': 'Plateforme de Réservation Nouakchott API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'hotels': '/api/hotels/',
            'apartments': '/api/apartments/',
            'reservations': '/api/reservations/',
            'users': '/api/users/',
            'admin': '/admin/',
        }
    })

def home(request):
    """Vue de base pour la racine"""
    return JsonResponse({
        'message': 'Plateforme de Réservation Nouakchott',
        'api': '/api/',
        'admin': '/admin/',
        'frontend': 'http://localhost:3000'
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/', api_root, name='api_root'),
    path('api/', include([
        # Authentication (custom + JWT under /jwt/)
        path('auth/', include(('users.urls', 'users'), namespace='users_auth')),
        path('auth/jwt/', include([
            path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        ])),
        # Alias expected by frontend
        path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh_alias'),
        
        # Hotels
        path('hotels/', include(('hotels.urls', 'hotels'), namespace='hotels_root')),
        
        # Apartments
        path('apartments/', include(('apartments.urls', 'apartments'), namespace='apartments_root')),
        
        # Reservations
        path('reservations/', include(('reservations.urls', 'reservations'), namespace='reservations_root')),
        # Payments alias expected by frontend
        path('payments/', include([
            path('', reservation_views.PaymentListView.as_view(), name='payment_list_root'),
            path('<int:pk>/', reservation_views.PaymentDetailView.as_view(), name='payment_detail_root'),
        ])),
        
        # Users (admin)
        path('users/', include(('users.urls', 'users'), namespace='users_admin')),
        
        # Dashboard (admin)
        path('dashboard/', include(('reservations.urls', 'reservations'), namespace='reservations_dashboard')),
        
        # Search alias expected by frontend
        path('search/', hotel_views.HotelSearchView.as_view(), name='search_root'),
        
        # Upload alias expected by frontend
        path('upload/', hotel_views.unified_upload, name='unified_upload'),
        
        # Settings
        path('settings/', include(('users.urls', 'users'), namespace='users_settings')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
