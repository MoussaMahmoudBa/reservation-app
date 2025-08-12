from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Apartment, ApartmentImage, ApartmentReview, ApartmentAvailability


class ApartmentImageInline(admin.TabularInline):
    """Inline pour les images d'appartement"""
    model = ApartmentImage
    extra = 1
    fields = ('image', 'caption', 'is_primary', 'order')


class ApartmentAvailabilityInline(admin.TabularInline):
    """Inline pour les disponibilités d'appartement"""
    model = ApartmentAvailability
    extra = 1
    fields = ('date', 'is_available', 'price_override', 'notes')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """Interface d'administration pour les appartements"""
    
    list_display = ('name', 'apartment_type', 'bedrooms', 'bathrooms', 'rating', 'price_per_night', 'is_active', 'is_featured')
    list_filter = ('apartment_type', 'property_type', 'is_active', 'is_featured', 'city', 'wifi', 'air_conditioning', 'pool', 'created_at')
    search_fields = ('name', 'address', 'city', 'owner__username', 'owner__email')
    ordering = ('-rating', '-created_at')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('name', 'description', 'address', 'city', 'country', 'latitude', 'longitude')
        }),
        (_('Caractéristiques'), {
            'fields': ('apartment_type', 'property_type', 'bedrooms', 'bathrooms', 'max_guests', 'surface_area', 'floor')
        }),
        (_('Prix'), {
            'fields': ('price_per_night', 'discount_percentage', 'cleaning_fee', 'service_fee')
        }),
        (_('Équipements'), {
            'fields': (
                'wifi', 'air_conditioning', 'heating', 'kitchen', 'washing_machine', 'dryer',
                'tv', 'balcony', 'terrace', 'garden', 'parking', 'elevator', 'pool', 'gym'
            )
        }),
        (_('Évaluations'), {
            'fields': ('rating', 'total_reviews')
        }),
        (_('Statut'), {
            'fields': ('is_active', 'is_featured', 'is_instant_bookable')
        }),
        (_('Propriétaire'), {
            'fields': ('owner',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ApartmentImageInline, ApartmentAvailabilityInline]
    readonly_fields = ('rating', 'total_reviews', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')


@admin.register(ApartmentReview)
class ApartmentReviewAdmin(admin.ModelAdmin):
    """Interface d'administration pour les avis d'appartements"""
    
    list_display = ('apartment', 'user', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('apartment__name', 'user__username', 'title', 'comment')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('apartment', 'user', 'rating', 'title', 'comment')
        }),
        (_('Statut'), {
            'fields': ('is_verified',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('apartment', 'user')


@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
    """Interface d'administration pour les images d'appartements"""
    
    list_display = ('apartment', 'caption', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('apartment__name', 'caption')
    ordering = ('apartment__name', 'order')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('apartment', 'image', 'caption')
        }),
        (_('Affichage'), {
            'fields': ('is_primary', 'order')
        }),
        (_('Métadonnées'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('apartment')


@admin.register(ApartmentAvailability)
class ApartmentAvailabilityAdmin(admin.ModelAdmin):
    """Interface d'administration pour les disponibilités d'appartements"""
    
    list_display = ('apartment', 'date', 'is_available', 'price_override', 'notes')
    list_filter = ('is_available', 'date', 'apartment')
    search_fields = ('apartment__name', 'notes')
    ordering = ('apartment__name', 'date')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('apartment', 'date', 'is_available')
        }),
        (_('Prix spécial'), {
            'fields': ('price_override', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('apartment')
