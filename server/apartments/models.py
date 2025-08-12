from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Apartment(models.Model):
    """Modèle pour les appartements"""
    
    APARTMENT_TYPES = [
        ('studio', _('Studio')),
        ('one_bedroom', _('1 chambre')),
        ('two_bedroom', _('2 chambres')),
        ('three_bedroom', _('3 chambres')),
        ('four_bedroom', _('4 chambres')),
        ('penthouse', _('Penthouse')),
        ('villa', _('Villa')),
    ]
    
    PROPERTY_TYPES = [
        ('apartment', _('Appartement')),
        ('house', _('Maison')),
        ('villa', _('Villa')),
        ('studio', _('Studio')),
    ]
    
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'))
    address = models.TextField(_('adresse'))
    city = models.CharField(_('ville'), max_length=100, default='Nouakchott')
    country = models.CharField(_('pays'), max_length=100, default='Mauritanie')
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Caractéristiques
    apartment_type = models.CharField(_('type d\'appartement'), max_length=20, choices=APARTMENT_TYPES)
    property_type = models.CharField(_('type de propriété'), max_length=20, choices=PROPERTY_TYPES)
    bedrooms = models.IntegerField(_('chambres'), default=1)
    bathrooms = models.IntegerField(_('salles de bain'), default=1)
    max_guests = models.IntegerField(_('nombre maximum de voyageurs'), default=2)
    surface_area = models.IntegerField(_('surface en m²'), null=True, blank=True)
    floor = models.IntegerField(_('étage'), null=True, blank=True)
    
    # Prix
    price_per_night = models.DecimalField(_('prix par nuit'), max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        _('pourcentage de réduction'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    cleaning_fee = models.DecimalField(_('frais de ménage'), max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(_('frais de service'), max_digits=10, decimal_places=2, default=0.00)
    
    # Équipements
    wifi = models.BooleanField(_('Wi-Fi'), default=True)
    air_conditioning = models.BooleanField(_('climatisation'), default=True)
    heating = models.BooleanField(_('chauffage'), default=False)
    kitchen = models.BooleanField(_('cuisine équipée'), default=True)
    washing_machine = models.BooleanField(_('machine à laver'), default=False)
    dryer = models.BooleanField(_('sèche-linge'), default=False)
    tv = models.BooleanField(_('télévision'), default=True)
    balcony = models.BooleanField(_('balcon'), default=False)
    terrace = models.BooleanField(_('terrasse'), default=False)
    garden = models.BooleanField(_('jardin'), default=False)
    parking = models.BooleanField(_('parking'), default=False)
    elevator = models.BooleanField(_('ascenseur'), default=False)
    pool = models.BooleanField(_('piscine'), default=False)
    gym = models.BooleanField(_('salle de sport'), default=False)
    
    # Évaluations
    rating = models.DecimalField(
        _('note moyenne'),
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(_('nombre total d\'avis'), default=0)
    
    # Statut
    is_active = models.BooleanField(_('actif'), default=True)
    is_featured = models.BooleanField(_('mis en avant'), default=False)
    is_instant_bookable = models.BooleanField(_('réservation instantanée'), default=True)
    
    # Propriétaire
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_apartments'
    )
    
    # Métadonnées
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    class Meta:
        verbose_name = _('appartement')
        verbose_name_plural = _('appartements')
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_apartment_type_display()})"
    
    @property
    def discounted_price(self):
        """Prix avec réduction appliquée"""
        if self.discount_percentage > 0:
            discount = self.price_per_night * (self.discount_percentage / 100)
            return self.price_per_night - discount
        return self.price_per_night
    
    @property
    def total_price_per_night(self):
        """Prix total par nuit incluant tous les frais"""
        return self.discounted_price + self.cleaning_fee + self.service_fee
    
    def update_rating(self):
        """Mettre à jour la note moyenne basée sur les avis"""
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            self.rating = total_rating / reviews.count()
            self.total_reviews = reviews.count()
        else:
            self.rating = 0.00
            self.total_reviews = 0
        self.save()


class ApartmentImage(models.Model):
    """Images pour les appartements"""
    
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.URLField(_('image'), max_length=500)  # Changé pour accepter les URLs Cloudinary
    caption = models.CharField(_('légende'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('image principale'), default=False)
    order = models.IntegerField(_('ordre'), default=0)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('image d\'appartement')
        verbose_name_plural = _('images d\'appartements')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image de {self.apartment.name}"


class ApartmentReview(models.Model):
    """Avis sur les appartements"""
    
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='apartment_reviews'
    )
    rating = models.IntegerField(
        _('note'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(_('titre'), max_length=200)
    comment = models.TextField(_('commentaire'))
    is_verified = models.BooleanField(_('vérifié'), default=False)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    class Meta:
        verbose_name = _('avis d\'appartement')
        verbose_name_plural = _('avis d\'appartements')
        ordering = ['-created_at']
        unique_together = ['apartment', 'user']
    
    def __str__(self):
        return f"Avis de {self.user.username} sur {self.apartment.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour la note moyenne de l'appartement
        self.apartment.update_rating()


class ApartmentAvailability(models.Model):
    """Disponibilité des appartements"""
    
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='availability'
    )
    date = models.DateField(_('date'))
    is_available = models.BooleanField(_('disponible'), default=True)
    price_override = models.DecimalField(
        _('prix spécial'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('disponibilité d\'appartement')
        verbose_name_plural = _('disponibilités d\'appartements')
        unique_together = ['apartment', 'date']
        ordering = ['date']
    
    def __str__(self):
        return f"{self.apartment.name} - {self.date}"
