from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Hotel(models.Model):
    """Modèle pour les hôtels"""
    
    STARS_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]
    
    name = models.CharField(_('nom'), max_length=200)
    description = models.TextField(_('description'))
    address = models.TextField(_('adresse'))
    city = models.CharField(_('ville'), max_length=100, default='Nouakchott')
    country = models.CharField(_('pays'), max_length=100, default='Mauritanie')
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(_('téléphone'), max_length=20)
    email = models.EmailField(_('email'))
    
    # Classification
    stars = models.IntegerField(_('étoiles'), choices=STARS_CHOICES, default=3)
    rating = models.DecimalField(
        _('note moyenne'),
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(_('nombre total d\'avis'), default=0)
    
    # Services
    wifi = models.BooleanField(_('Wi-Fi'), default=True)
    air_conditioning = models.BooleanField(_('climatisation'), default=True)
    restaurant = models.BooleanField(_('restaurant'), default=False)
    pool = models.BooleanField(_('piscine'), default=False)
    gym = models.BooleanField(_('salle de sport'), default=False)
    spa = models.BooleanField(_('spa'), default=False)
    parking = models.BooleanField(_('parking'), default=True)
    airport_shuttle = models.BooleanField(_('navette aéroport'), default=False)
    
    # Statut
    is_active = models.BooleanField(_('actif'), default=True)
    is_featured = models.BooleanField(_('mis en avant'), default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_hotels'
    )
    
    class Meta:
        verbose_name = _('hôtel')
        verbose_name_plural = _('hôtels')
        ordering = ['-rating', '-stars', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.stars} étoiles)"
    
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


class HotelImage(models.Model):
    """Images pour les hôtels"""
    
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.URLField(_('image'), max_length=500)  # Changé pour accepter les URLs Cloudinary
    caption = models.CharField(_('légende'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('image principale'), default=False)
    order = models.IntegerField(_('ordre'), default=0)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('image d\'hôtel')
        verbose_name_plural = _('images d\'hôtels')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image de {self.hotel.name}"


class RoomType(models.Model):
    """Types de chambres dans un hôtel"""
    
    ROOM_CATEGORIES = [
        ('single', _('Chambre simple')),
        ('double', _('Chambre double')),
        ('twin', _('Chambre twin')),
        ('triple', _('Chambre triple')),
        ('suite', _('Suite')),
        ('family', _('Chambre familiale')),
        ('luxury', _('Chambre de luxe')),
    ]
    
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='room_types'
    )
    name = models.CharField(_('nom'), max_length=100)
    category = models.CharField(_('catégorie'), max_length=20, choices=ROOM_CATEGORIES)
    description = models.TextField(_('description'))
    capacity = models.IntegerField(_('capacité'), default=2)
    price_per_night = models.DecimalField(_('prix par nuit'), max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        _('pourcentage de réduction'),
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    is_available = models.BooleanField(_('disponible'), default=True)
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    class Meta:
        verbose_name = _('type de chambre')
        verbose_name_plural = _('types de chambres')
        ordering = ['price_per_night']
    
    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
    
    @property
    def discounted_price(self):
        """Prix avec réduction appliquée"""
        if self.discount_percentage > 0:
            discount = self.price_per_night * (self.discount_percentage / 100)
            return self.price_per_night - discount
        return self.price_per_night


class HotelReview(models.Model):
    """Avis sur les hôtels"""
    
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hotel_reviews'
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
        verbose_name = _('avis d\'hôtel')
        verbose_name_plural = _('avis d\'hôtels')
        ordering = ['-created_at']
        unique_together = ['hotel', 'user']
    
    def __str__(self):
        return f"Avis de {self.user.username} sur {self.hotel.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour la note moyenne de l'hôtel
        self.hotel.update_rating()
