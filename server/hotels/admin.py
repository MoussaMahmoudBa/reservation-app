from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Hotel, HotelImage, RoomType, HotelReview


class HotelImageInline(admin.TabularInline):
    """Inline pour les images d'hôtel"""
    model = HotelImage
    extra = 1
    fields = ('image', 'caption', 'is_primary', 'order')


class RoomTypeInline(admin.TabularInline):
    """Inline pour les types de chambres"""
    model = RoomType
    extra = 1
    fields = ('name', 'category', 'capacity', 'price_per_night', 'discount_percentage', 'is_available')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Interface d'administration pour les hôtels"""
    
    list_display = ('name', 'stars', 'rating', 'city', 'is_active', 'is_featured', 'created_at')
    list_filter = ('stars', 'is_active', 'is_featured', 'city', 'wifi', 'air_conditioning', 'pool', 'created_at')
    search_fields = ('name', 'address', 'city', 'phone', 'email')
    ordering = ('-rating', '-stars', 'name')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('name', 'description', 'address', 'city', 'country', 'latitude', 'longitude')
        }),
        (_('Contact'), {
            'fields': ('phone', 'email')
        }),
        (_('Classification'), {
            'fields': ('stars', 'rating', 'total_reviews')
        }),
        (_('Services'), {
            'fields': (
                'wifi', 'air_conditioning', 'restaurant', 'pool', 'gym', 'spa', 
                'parking', 'airport_shuttle'
            )
        }),
        (_('Statut'), {
            'fields': ('is_active', 'is_featured')
        }),
        (_('Métadonnées'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [HotelImageInline, RoomTypeInline]
    readonly_fields = ('rating', 'total_reviews', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """Interface d'administration pour les types de chambres"""
    
    list_display = ('name', 'hotel', 'category', 'capacity', 'price_per_night', 'discounted_price', 'is_available')
    list_filter = ('category', 'is_available', 'hotel', 'created_at')
    search_fields = ('name', 'hotel__name')
    ordering = ('hotel__name', 'price_per_night')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('hotel', 'name', 'category', 'description', 'capacity')
        }),
        (_('Prix'), {
            'fields': ('price_per_night', 'discount_percentage')
        }),
        (_('Statut'), {
            'fields': ('is_available',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('hotel')


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    """Interface d'administration pour les avis d'hôtels"""
    
    list_display = ('hotel', 'user', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('hotel__name', 'user__username', 'title', 'comment')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('hotel', 'user', 'rating', 'title', 'comment')
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
        return super().get_queryset(request).select_related('hotel', 'user')


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    """Interface d'administration pour les images d'hôtels"""
    
    list_display = ('hotel', 'caption', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('hotel__name', 'caption')
    ordering = ('hotel__name', 'order')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('hotel', 'image', 'caption')
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
        return super().get_queryset(request).select_related('hotel')
