from rest_framework import serializers
from .models import Apartment, ApartmentImage, ApartmentReview, ApartmentAvailability
from users.serializers import UserSerializer


class ApartmentImageSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les images d'appartements
    """
    class Meta:
        model = ApartmentImage
        fields = ['id', 'apartment', 'image', 'caption', 'is_primary', 'created_at']


class ApartmentReviewSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les avis d'appartements
    """
    user = UserSerializer(read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ApartmentReview
        fields = ['id', 'apartment', 'user', 'user_name', 'rating', 'title', 'comment', 'created_at']
        read_only_fields = ['user', 'apartment', 'created_at']


class ApartmentAvailabilitySerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la disponibilité des appartements
    """
    class Meta:
        model = ApartmentAvailability
        fields = ['id', 'apartment', 'start_date', 'end_date', 'is_available', 'price_override', 'notes']


class ApartmentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur principal pour les appartements
    """
    images = ApartmentImageSerializer(many=True, read_only=True)
    reviews = ApartmentReviewSerializer(many=True, read_only=True)
    availability = ApartmentAvailabilitySerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'name', 'description', 'address', 'city',
            'apartment_type', 'property_type', 'bedrooms', 'bathrooms',
            'max_guests', 'price_per_night', 'latitude', 'longitude',
            'surface_area', 'floor', 'discount_percentage', 'cleaning_fee', 'service_fee',
            'wifi', 'air_conditioning', 'heating', 'kitchen', 'washing_machine',
            'dryer', 'tv', 'balcony', 'terrace', 'garden', 'parking', 'elevator',
            'pool', 'gym', 'owner', 'images', 'reviews', 'availability', 'rating',
            'total_reviews', 'is_active', 'is_featured', 'is_instant_bookable',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'rating', 'total_reviews', 'created_at', 'updated_at']


class ApartmentCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'appartements
    """
    image_urls = serializers.ListField(
        child=serializers.CharField(max_length=500),
        required=False,
        write_only=True
    )
    
    def validate_image_urls(self, value):
        """Validation simplifiée pour les URLs d'images"""
        if not value:
            return value
            
        for url in value:
            if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                raise serializers.ValidationError(f"URL invalide: {url}")
        return value
    
    class Meta:
        model = Apartment
        fields = [
            'id', 'name', 'description', 'address', 'city',
            'apartment_type', 'property_type', 'bedrooms', 'bathrooms',
            'max_guests', 'price_per_night', 'latitude', 'longitude',
            'surface_area', 'floor', 'discount_percentage', 'cleaning_fee', 'service_fee',
            'wifi', 'air_conditioning', 'heating', 'kitchen', 'washing_machine',
            'dryer', 'tv', 'balcony', 'terrace', 'garden', 'parking', 'elevator',
            'pool', 'gym', 'is_active', 'is_featured', 'is_instant_bookable',
            'image_urls'
        ]
    
    def create(self, validated_data):
        image_urls = validated_data.pop('image_urls', [])
        validated_data['owner'] = self.context['request'].user
        apartment = super().create(validated_data)
        
        # Créer les images
        for i, image_url in enumerate(image_urls):
            ApartmentImage.objects.create(
                apartment=apartment,
                image=image_url,
                is_primary=(i == 0),  # La première image est principale
                order=i
            )
        
        return apartment
        

class ApartmentUpdateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la modification d'appartements
    """
    class Meta:
        model = Apartment
        fields = [
            'name', 'description', 'address', 'city',
            'apartment_type', 'property_type', 'bedrooms', 'bathrooms',
            'max_guests', 'price_per_night', 'latitude', 'longitude',
            'surface_area', 'floor', 'discount_percentage', 'cleaning_fee', 'service_fee',
            'wifi', 'air_conditioning', 'heating', 'kitchen', 'washing_machine',
            'dryer', 'tv', 'balcony', 'terrace', 'garden', 'parking', 'elevator',
            'pool', 'gym', 'is_active', 'is_featured', 'is_instant_bookable'
        ]


class ApartmentSearchSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la recherche d'appartements
    """
    images = ApartmentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'name', 'description', 'address', 'city',
            'apartment_type', 'property_type', 'bedrooms', 'bathrooms',
            'max_guests', 'price_per_night', 'latitude', 'longitude',
            'surface_area', 'floor', 'discount_percentage', 'cleaning_fee', 'service_fee',
            'wifi', 'air_conditioning', 'heating', 'kitchen', 'washing_machine',
            'dryer', 'tv', 'balcony', 'terrace', 'garden', 'parking', 'elevator',
            'pool', 'gym', 'rating', 'total_reviews', 'is_active', 'is_featured',
            'is_instant_bookable', 'images', 'created_at'
        ]


class ApartmentStatsSerializer(serializers.Serializer):
    """
    Sérialiseur pour les statistiques des appartements
    """
    total_apartments = serializers.IntegerField()
    active_apartments = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    apartments_by_type = serializers.DictField()
    apartments_by_city = serializers.DictField()
    price_range = serializers.DictField() 