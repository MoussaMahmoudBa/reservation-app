from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from users.models import User
from hotels.models import Hotel, RoomType
from apartments.models import Apartment


class Reservation(models.Model):
    """Modèle pour les réservations"""
    
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('confirmed', _('Confirmée')),
        ('cancelled', _('Annulée')),
        ('completed', _('Terminée')),
        ('refunded', _('Remboursée')),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('paid', _('Payée')),
        ('failed', _('Échouée')),
        ('refunded', _('Remboursée')),
    ]
    
    # Informations de base
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    reservation_number = models.CharField(_('numéro de réservation'), max_length=20, unique=True)
    
    # Dates
    check_in_date = models.DateField(_('date d\'arrivée'))
    check_out_date = models.DateField(_('date de départ'))
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    # Informations des voyageurs
    guest_name = models.CharField(_('nom du voyageur'), max_length=200)
    guest_email = models.EmailField(_('email du voyageur'))
    guest_phone = models.CharField(_('téléphone du voyageur'), max_length=20)
    number_of_guests = models.IntegerField(_('nombre de voyageurs'), default=1)
    special_requests = models.TextField(_('demandes spéciales'), blank=True)
    
    # Prix et paiement
    total_amount = models.DecimalField(_('montant total'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('montant des taxes'), max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(_('montant de la réduction'), max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(_('montant final'), max_digits=10, decimal_places=2)
    
    # Statuts
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('statut du paiement'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Métadonnées
    is_cancelled = models.BooleanField(_('annulée'), default=False)
    cancellation_reason = models.TextField(_('raison de l\'annulation'), blank=True)
    cancelled_at = models.DateTimeField(_('annulée le'), null=True, blank=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_reservations'
    )
    
    class Meta:
        verbose_name = _('réservation')
        verbose_name_plural = _('réservations')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Réservation {self.reservation_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            # Générer un numéro de réservation unique
            import uuid
            self.reservation_number = f"RES-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculer le montant final
        tax_amount = self.tax_amount or 0
        discount_amount = self.discount_amount or 0
        self.final_amount = self.total_amount + tax_amount - discount_amount
        
        super().save(*args, **kwargs)
    
    @property
    def number_of_nights(self):
        """Calculer le nombre de nuits"""
        from datetime import date
        return (self.check_out_date - self.check_in_date).days
    
    @property
    def is_active(self):
        """Vérifier si la réservation est active"""
        from datetime import date
        today = date.today()
        return (
            self.status in ['pending', 'confirmed'] and
            not self.is_cancelled and
            self.check_out_date >= today
        )
    
    @property
    def can_be_cancelled(self):
        """Vérifier si la réservation peut être annulée"""
        from datetime import date, timedelta
        today = date.today()
        # Permettre l'annulation jusqu'à 24h avant l'arrivée
        return (
            self.status in ['pending', 'confirmed'] and
            not self.is_cancelled and
            self.check_in_date > today + timedelta(days=1)
        )


class HotelReservation(Reservation):
    """Réservation d'hôtel"""
    
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    
    class Meta:
        verbose_name = _('réservation d\'hôtel')
        verbose_name_plural = _('réservations d\'hôtels')
    
    def __str__(self):
        return f"Réservation hôtel {self.reservation_number} - {self.hotel.name}"


class ApartmentReservation(Reservation):
    """Réservation d'appartement"""
    
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    
    class Meta:
        verbose_name = _('réservation d\'appartement')
        verbose_name_plural = _('réservations d\'appartements')
    
    def __str__(self):
        return f"Réservation appartement {self.reservation_number} - {self.apartment.name}"


class Payment(models.Model):
    """Modèle pour les paiements"""
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', _('Carte de crédit')),
        ('debit_card', _('Carte de débit')),
        ('bank_transfer', _('Virement bancaire')),
        ('mobile_money', _('Mobile Money')),
        ('cash', _('Espèces')),
        ('paypal', _('PayPal')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('processing', _('En cours')),
        ('completed', _('Terminé')),
        ('failed', _('Échoué')),
        ('refunded', _('Remboursé')),
    ]
    
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(_('montant'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('méthode de paiement'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Informations de transaction
    transaction_id = models.CharField(_('ID de transaction'), max_length=100, blank=True)
    payment_gateway = models.CharField(_('passerelle de paiement'), max_length=50, blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    processed_at = models.DateTimeField(_('traité le'), null=True, blank=True)
    
    # Informations d'erreur
    error_message = models.TextField(_('message d\'erreur'), blank=True)
    
    class Meta:
        verbose_name = _('paiement')
        verbose_name_plural = _('paiements')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Paiement {self.transaction_id} - {self.reservation.reservation_number}"


class CancellationPolicy(models.Model):
    """Politique d'annulation"""
    
    name = models.CharField(_('nom'), max_length=100)
    description = models.TextField(_('description'))
    
    # Délais d'annulation
    free_cancellation_hours = models.IntegerField(
        _('heures d\'annulation gratuite'),
        default=24,
        help_text=_('Nombre d\'heures avant l\'arrivée pour une annulation gratuite')
    )
    
    # Pourcentages de remboursement
    refund_percentage_24h = models.DecimalField(
        _('remboursement 24h avant'),
        max_digits=5,
        decimal_places=2,
        default=100.00,
        help_text=_('Pourcentage de remboursement 24h avant l\'arrivée')
    )
    refund_percentage_48h = models.DecimalField(
        _('remboursement 48h avant'),
        max_digits=5,
        decimal_places=2,
        default=50.00,
        help_text=_('Pourcentage de remboursement 48h avant l\'arrivée')
    )
    refund_percentage_72h = models.DecimalField(
        _('remboursement 72h avant'),
        max_digits=5,
        decimal_places=2,
        default=25.00,
        help_text=_('Pourcentage de remboursement 72h avant l\'arrivée')
    )
    
    is_active = models.BooleanField(_('actif'), default=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('politique d\'annulation')
        verbose_name_plural = _('politiques d\'annulation')
    
    def __str__(self):
        return self.name
    
    def get_refund_percentage(self, hours_before_checkin):
        """Obtenir le pourcentage de remboursement selon les heures avant l'arrivée"""
        if hours_before_checkin >= 72:
            return self.refund_percentage_72h
        elif hours_before_checkin >= 48:
            return self.refund_percentage_48h
        elif hours_before_checkin >= 24:
            return self.refund_percentage_24h
        else:
            return 0.00
