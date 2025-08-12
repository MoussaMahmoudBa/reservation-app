from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est un administrateur.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour permettre l'accès au propriétaire ou à l'administrateur.
    """
    
    def has_object_permission(self, request, view, obj):
        # L'administrateur a toujours accès
        if request.user.is_admin:
            return True
        
        # Le propriétaire a accès à son propre objet
        return obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre la lecture à tous et l'écriture au propriétaire.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture autorisée seulement au propriétaire ou à l'administrateur
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_admin
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_admin
        else:
            return obj == request.user or request.user.is_admin


class IsVerifiedUser(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est vérifié.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verified


class IsActiveUser(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est actif.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active 