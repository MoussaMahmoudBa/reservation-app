from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Interface d'administration pour les utilisateurs"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_verified', 'preferred_language', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'profile_picture')
        }),
        (_('Type d\'utilisateur'), {
            'fields': ('user_type', 'is_verified')
        }),
        (_('Préférences'), {
            'fields': ('preferred_language', 'notification_email', 'notification_sms')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
