from rest_framework import serializers
from .models import Hotel, HotelImage, RoomType, HotelReview
from users.serializers import UserSerializer


class HotelImageSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les images d'hôtel"""
    
    class Meta:
        model = HotelImage
        fields = [
            'id', 'hotel', 'image', 'caption', 'is_primary', 
            'order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RoomTypeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les types de chambres"""
    
    class Meta:
        model = RoomType
        fields = [
            'id', 'hotel', 'name', 'category', 'description', 'capacity',
            'price_per_night', 'discount_percentage', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HotelReviewSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les avis d'hôtel"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = HotelReview
        fields = [
            'id', 'hotel', 'user', 'rating', 'title', 'comment',
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified', 'created_at', 'updated_at']


class HotelSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les hôtels"""
    images = HotelImageSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    reviews = HotelReviewSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'address', 'city', 'country',
            'latitude', 'longitude', 'phone', 'email',
            'stars', 'rating', 'total_reviews', 'wifi', 'air_conditioning',
            'restaurant', 'pool', 'gym', 'spa', 'parking', 'airport_shuttle',
            'is_active', 'is_featured', 'created_by', 'created_at', 'updated_at',
            'images', 'room_types', 'reviews'
        ]
        read_only_fields = [
            'id', 'rating', 'total_reviews', 'created_at', 'updated_at',
            'images', 'room_types', 'reviews'
        ]


class RoomTypeCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création de types de chambres (sans hotel requis)"""
    
    class Meta:
        model = RoomType
        fields = [
            'name', 'category', 'description', 'capacity',
            'price_per_night', 'discount_percentage', 'is_available'
        ]


class HotelCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la création d'hôtels"""
    room_types = RoomTypeCreateSerializer(many=True, required=False)
    image_urls = serializers.ListField(
        child=serializers.CharField(max_length=500),
        required=False,
        write_only=True
    )
    
    def validate_image_urls(self, value):
        """Validation simplifiée pour les URLs d'images"""
        print(f"DEBUG: validate_image_urls called with value: {value}")
        print(f"DEBUG: Type of value: {type(value)}")
        
        if not value:
            print("DEBUG: No image_urls provided")
            return value
            
        for i, url in enumerate(value):
            print(f"DEBUG: Validating URL {i}: {url}")
            print(f"DEBUG: URL type: {type(url)}")
            if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                print(f"DEBUG: URL validation failed for: {url}")
                raise serializers.ValidationError(f"URL invalide: {url}")
            else:
                print(f"DEBUG: URL validation passed for: {url}")
        return value
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'address', 'city', 'country',
            'latitude', 'longitude', 'phone', 'email',
            'stars', 'wifi', 'air_conditioning', 'restaurant', 'pool',
            'gym', 'spa', 'parking', 'airport_shuttle', 'is_featured',
            'room_types', 'image_urls'
        ]
    
    def create(self, validated_data):
        room_types_data = validated_data.pop('room_types', [])
        image_urls = validated_data.pop('image_urls', [])
        validated_data['created_by'] = self.context['request'].user
        hotel = super().create(validated_data)
        
        # Créer les types de chambres
        for room_type_data in room_types_data:
            room_type_data['hotel'] = hotel
            RoomType.objects.create(**room_type_data)
        
        # Créer les images
        for i, image_url in enumerate(image_urls):
            HotelImage.objects.create(
                hotel=hotel,
                image=image_url,
                is_primary=(i == 0),  # La première image est principale
                order=i
            )
        
        return hotel

class HotelUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour d'hôtels"""
    
    class Meta:
        model = Hotel
        fields = [
            'name', 'description', 'address', 'city', 'country',
            'latitude', 'longitude', 'phone', 'email',
            'stars', 'wifi', 'air_conditioning', 'restaurant', 'pool',
            'gym', 'spa', 'parking', 'airport_shuttle', 'is_active', 'is_featured'
        ]


class HotelSearchSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la recherche d'hôtels"""
    images = HotelImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'address', 'city', 'country',
            'stars', 'rating', 'total_reviews', 'wifi', 'air_conditioning',
            'restaurant', 'pool', 'gym', 'spa', 'parking', 'airport_shuttle',
            'is_featured', 'images'
        ]
        read_only_fields = ['id', 'rating', 'total_reviews', 'images']


class HotelStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques des hôtels"""
    total_hotels = serializers.IntegerField()
    active_hotels = serializers.IntegerField()
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    hotels_by_stars = serializers.DictField()
    hotels_by_city = serializers.DictField() 