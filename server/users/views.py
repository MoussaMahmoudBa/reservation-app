from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db import transaction
from .models import User, PasswordResetOTP
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ProfileSerializer,
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetVerifySerializer,
)
from .permissions import IsAdminUser, IsOwnerOrAdmin
from .utils import normalize_phone, generate_otp, get_default_otp_expiry, send_sms


class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Utilisateur créé avec succès',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateUserView(generics.CreateAPIView):
    """Vue pour la création d'utilisateurs par les admins"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Utilisateur créé avec succès',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Erreur lors de la création',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour récupérer et mettre à jour le profil utilisateur"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour le profil utilisateur"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """Vue pour lister les utilisateurs (admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['user_type', 'is_active', 'is_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'username', 'email']


class UserDetailView(generics.RetrieveUpdateAPIView):
    """Vue pour récupérer et mettre à jour les détails d'un utilisateur"""
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class UserUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour un utilisateur (admin)"""
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Protection : empêcher la désactivation de son propre compte administrateur
        if 'is_active' in request.data and not request.data['is_active']:
            if instance.id == request.user.id:
                return Response({
                    'message': 'Vous ne pouvez pas désactiver votre propre compte administrateur',
                    'error': 'self_deactivation_forbidden'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Protection supplémentaire : empêcher la désactivation d'autres superusers
            if instance.is_superuser and not request.user.is_superuser:
                return Response({
                    'message': 'Vous ne pouvez pas désactiver un autre superutilisateur',
                    'error': 'superuser_deactivation_forbidden'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'message': 'Utilisateur mis à jour avec succès',
            'user': UserSerializer(instance).data
        })


class UserDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer un utilisateur (admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Protection : empêcher la suppression de son propre compte
        if user.id == request.user.id:
            return Response({
                'message': 'Vous ne pouvez pas supprimer votre propre compte',
                'error': 'self_deletion_forbidden'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Protection : empêcher la suppression d'autres superusers
        if user.is_superuser and not request.user.is_superuser:
            return Response({
                'message': 'Vous ne pouvez pas supprimer un autre superutilisateur',
                'error': 'superuser_deletion_forbidden'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()
        return Response({
            'message': 'Utilisateur désactivé avec succès'
        }, status=status.HTTP_200_OK)


class SettingsView(APIView):
    """Vue pour récupérer les paramètres de l'application"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Ici vous pouvez retourner les paramètres de l'application
        settings = {
            'site_name': 'Plateforme de Réservation Nouakchott',
            'contact_email': 'contact@nouakchott-reservation.com',
            'support_phone': '+222 123 456 789',
            'currency': 'MRU',
            'timezone': 'Africa/Nouakchott',
            'languages': ['fr', 'en', 'ar'],
            'default_language': 'fr',
        }
        return Response(settings)


class SettingsUpdateView(APIView):
    """Vue pour mettre à jour les paramètres de l'application (admin)"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def patch(self, request):
        # Ici vous pouvez mettre à jour les paramètres de l'application
        return Response({
            'message': 'Paramètres mis à jour avec succès'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Vue personnalisée pour la connexion par téléphone"""
    phone = request.data.get('phone')
    password = request.data.get('password')
    
    if not phone or not password:
        return Response({
            'error': 'Numéro de téléphone et mot de passe requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    phone = normalize_phone(phone)
    
    user = authenticate(username=phone, password=password)
    
    if user is None:
        return Response({
            'error': 'Numéro de téléphone ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            'error': 'Compte désactivé'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Générer les tokens
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Vue pour la déconnexion"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Erreur lors de la déconnexion'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    """Vue pour demander la réinitialisation du mot de passe par téléphone"""
    serializer = PasswordResetSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            phone = serializer.validated_data['phone']  # déjà normalisé

            # Si un OTP non expiré existe déjà et non utilisé, on le réutilise pour éviter le spam
            existing = PasswordResetOTP.objects.filter(phone=phone, is_used=False).order_by('-created_at').first()
            if existing and not existing.is_expired():
                code = existing.code
                expires_at = existing.expires_at
            else:
                code = generate_otp(6)
                expires_at = get_default_otp_expiry(10)
                PasswordResetOTP.objects.create(
                    phone=phone,
                    code=code,
                    expires_at=expires_at,
                )

            # Envoyer le SMS
            send_sms(phone, f"Votre code de réinitialisation est {code}. Il expire dans 10 minutes.")

            return Response({
                'message': 'Code de vérification envoyé par SMS',
                'phone': phone,
                'expires_in_minutes': 10,
            }, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({
                'message': 'Échec d\'envoi du code',
                'errors': {'detail': str(exc)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Normaliser la forme des erreurs
    return Response({
        'message': 'Données invalides',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    """Vue pour confirmer la réinitialisation du mot de passe"""
    serializer = PasswordResetConfirmSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(phone=phone)

            otp = PasswordResetOTP.objects.filter(phone=phone, code=token, is_used=False).order_by('-created_at').first()
            if not otp:
                return Response({'message': 'Code de vérification invalide', 'errors': {'token': 'Code invalide'}}, status=status.HTTP_400_BAD_REQUEST)
            if otp.is_expired():
                return Response({'message': 'Code expiré', 'errors': {'token': 'Code expiré'}}, status=status.HTTP_400_BAD_REQUEST)

            # Mise à jour du mot de passe
            user.set_password(new_password)
            user.save()

            # Marquer l'OTP comme utilisé
            otp.is_used = True
            otp.save(update_fields=['is_used'])

            return Response({'message': 'Mot de passe réinitialisé avec succès'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'Utilisateur non trouvé', 'errors': {'phone': 'Utilisateur non trouvé'}}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Données invalides', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_verify(request):
    """Vérifie un OTP envoyé au téléphone sans changer le mot de passe."""
    serializer = PasswordResetVerifySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        token = serializer.validated_data['token']

        otp = PasswordResetOTP.objects.filter(phone=phone, code=token, is_used=False).order_by('-created_at').first()
        if not otp:
            return Response({'message': 'Code de vérification invalide', 'errors': {'token': 'Code invalide'}}, status=status.HTTP_400_BAD_REQUEST)
        if otp.is_expired():
            return Response({'message': 'Code expiré', 'errors': {'token': 'Code expiré'}}, status=status.HTTP_400_BAD_REQUEST)

        # Incrémente le nombre de tentatives uniquement lors des vérifications si nécessaire
        otp.attempts += 1
        otp.save(update_fields=['attempts'])

        return Response({'message': 'Code vérifié'}, status=status.HTTP_200_OK)

    return Response({'message': 'Données invalides', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
