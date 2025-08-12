from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Registration & Profile
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    
    # Password reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # User management (admin) - Ajout de l'endpoint racine
    path('', views.UserListView.as_view(), name='user_list_root'),
    path('create/', views.AdminCreateUserView.as_view(), name='admin_create_user'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Password reset verify
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
] 