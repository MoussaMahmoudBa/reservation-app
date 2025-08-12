from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import normalize_phone


class User(AbstractUser):
    """Modèle utilisateur personnalisé"""
    
    USER_TYPE_CHOICES = [
        ('client', _('Client')),
        ('admin', _('Administrateur')),
    ]
    
    # Rendre l'email optionnel et le téléphone obligatoire
    email = models.EmailField(_('adresse email'), blank=True, null=True)
    phone = models.CharField(_('téléphone'), max_length=20, unique=True)
    address = models.TextField(_('adresse'), blank=True)
    user_type = models.CharField(
        _('type d\'utilisateur'),
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='client'
    )
    profile_picture = models.ImageField(
        _('photo de profil'),
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(_('date de naissance'), blank=True, null=True)
    is_verified = models.BooleanField(_('vérifié'), default=False)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    # Champs pour les préférences
    preferred_language = models.CharField(
        _('langue préférée'),
        max_length=10,
        default='fr'
    )
    notification_email = models.BooleanField(_('notifications par email'), default=True)
    notification_sms = models.BooleanField(_('notifications par SMS'), default=False)
    
    # Utiliser le téléphone comme USERNAME_FIELD
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.phone})"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser

    def save(self, *args, **kwargs):
        # Normaliser le numéro avant sauvegarde
        if self.phone:
            self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)


class PasswordResetOTP(models.Model):
    """Stocke un OTP pour réinitialisation de mot de passe par téléphone."""
    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('OTP de réinitialisation')
        verbose_name_plural = _('OTPs de réinitialisation')
        indexes = [
            models.Index(fields=['phone', 'is_used']),
        ]

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at
    
    @property
    def is_client(self):
        return self.user_type == 'client'
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
