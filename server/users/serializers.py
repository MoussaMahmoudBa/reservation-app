from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import User
from .utils import normalize_phone, candidate_phone_variants

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'user_type', 'profile_picture',
            'date_of_birth', 'is_verified', 'is_active', 'preferred_language',
            'notification_email', 'notification_sms', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création d'utilisateurs"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'address',
            'user_type', 'date_of_birth', 'preferred_language',
            'notification_email', 'notification_sms', 'is_verified', 'is_active'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        phone_normalized = normalize_phone(attrs.get('phone', ''))
        if len(phone_normalized) != 12:  # +222 + 8 chiffres
            raise serializers.ValidationError("Numéro de téléphone invalide.")
        
        # Vérifier que le téléphone n'est pas déjà utilisé
        if User.objects.filter(phone=phone_normalized).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        
        # Vérifier que l'email n'est pas déjà utilisé (si fourni)
        if attrs.get('email') and User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        
        # Vérifier que le nom d'utilisateur n'est pas déjà utilisé
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        
        attrs['phone'] = phone_normalized
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        validated_data['phone'] = normalize_phone(validated_data.get('phone', ''))
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour d'utilisateurs"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'user_type', 'profile_picture',
            'date_of_birth', 'is_verified', 'is_active', 'preferred_language',
            'notification_email', 'notification_sms'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        phone_normalized = normalize_phone(value)
        if len(phone_normalized) != 12:
            raise serializers.ValidationError("Numéro de téléphone invalide.")
        return phone_normalized

    def update(self, instance, validated_data):
        # Normaliser le téléphone avant la mise à jour
        if 'phone' in validated_data:
            validated_data['phone'] = normalize_phone(validated_data['phone'])
        
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil utilisateur"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'profile_picture', 'date_of_birth',
            'preferred_language', 'notification_email', 'notification_sms'
        ]
        read_only_fields = ['username', 'phone']


class RegisterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'address',
            'user_type'
        ]
        extra_kwargs = {
            'user_type': {'default': 'client'},
            'email': {'required': False, 'allow_blank': True, 'allow_null': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
        phone_normalized = normalize_phone(attrs.get('phone', ''))
        if len(phone_normalized) != 12:
            raise serializers.ValidationError("Numéro de téléphone invalide.")
        
        # Vérifier que le téléphone n'est pas déjà utilisé
        if User.objects.filter(phone=phone_normalized).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        
        # Vérifier que l'email n'est pas déjà utilisé (si fourni)
        if attrs.get('email') and User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        
        # Vérifier que le nom d'utilisateur n'est pas déjà utilisé
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        
        attrs['phone'] = phone_normalized
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        validated_data['phone'] = normalize_phone(validated_data.get('phone', ''))
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Sérialiseur pour changer le mot de passe"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """Sérialiseur pour la réinitialisation du mot de passe par téléphone"""
    phone = serializers.CharField()
    
    def validate_phone(self, value):
        phone_normalized = normalize_phone(value)
        if len(phone_normalized) != 12:
            # tenter une recherche tolérante si format non strict
            variants = candidate_phone_variants(value)
            if not User.objects.filter(phone__in=[normalize_phone(v) for v in variants]).exists():
                raise serializers.ValidationError("Aucun utilisateur trouvé avec ce numéro de téléphone.")
            # retourner la forme canonique du premier match possible
            for v in variants:
                n = normalize_phone(v)
                if User.objects.filter(phone=n).exists():
                    return n
            return phone_normalized
        # format strict correct
        if not User.objects.filter(phone=phone_normalized).exists():
            raise serializers.ValidationError("Aucun utilisateur trouvé avec ce numéro de téléphone.")
        return phone_normalized


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Sérialiseur pour confirmer la réinitialisation du mot de passe"""
    phone = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        attrs['phone'] = normalize_phone(attrs.get('phone', ''))
        if len(attrs['phone']) != 12:
            raise serializers.ValidationError({"phone": "Numéro de téléphone invalide."})
        return attrs


class PasswordResetVerifySerializer(serializers.Serializer):
    """Sérialiseur pour vérifier un OTP sans changer le mot de passe."""
    phone = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        attrs['phone'] = normalize_phone(attrs.get('phone', ''))
        if len(attrs['phone']) != 12:
            raise serializers.ValidationError({"phone": "Numéro de téléphone invalide."})
        if not attrs.get('token'):
            raise serializers.ValidationError({"token": "Code requis."})
        return attrs


class UserStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques des utilisateurs"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    new_users_this_month = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    user_types = serializers.DictField()
    registration_trend = serializers.ListField() 