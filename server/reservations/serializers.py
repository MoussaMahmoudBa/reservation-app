from rest_framework import serializers
from .models import Reservation, HotelReservation, ApartmentReservation, Payment, CancellationPolicy
from users.serializers import UserSerializer
from hotels.serializers import HotelSerializer, RoomTypeSerializer
from apartments.serializers import ApartmentSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les paiements
    """
    class Meta:
        model = Payment
        fields = ['id', 'reservation', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['created_at']


class CancellationPolicySerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les politiques d'annulation
    """
    class Meta:
        model = CancellationPolicy
        fields = ['id', 'name', 'description', 'free_cancellation_hours', 'refund_percentages', 'created_at']
        read_only_fields = ['created_at']


class ReservationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de base pour les réservations
    """
    user = UserSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    cancellation_policy = CancellationPolicySerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'reservation_number', 'check_in_date', 'check_out_date',
            'number_of_guests', 'total_amount', 'status', 'special_requests',
            'payments', 'cancellation_policy', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reservation_number', 'created_at', 'updated_at']


class ReservationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de réservations
    """
    class Meta:
        model = Reservation
        fields = [
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_amount', 'special_requests', 'cancellation_policy'
        ]


class HotelReservationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les réservations d'hôtels
    """
    user = UserSerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)
    room_type = RoomTypeSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    cancellation_policy = CancellationPolicySerializer(read_only=True)

    class Meta:
        model = HotelReservation
        fields = [
            'id', 'user', 'hotel', 'room_type', 'reservation_number',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_amount', 'status', 'special_requests', 'payments',
            'cancellation_policy', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reservation_number', 'created_at', 'updated_at']


class HotelReservationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de réservations d'hôtels
    """
    class Meta:
        model = HotelReservation
        fields = [
            'hotel', 'room_type', 'check_in_date', 'check_out_date',
            'number_of_guests', 'total_amount', 'special_requests'
        ]


class ApartmentReservationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les réservations d'appartements
    """
    user = UserSerializer(read_only=True)
    apartment = ApartmentSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    cancellation_policy = CancellationPolicySerializer(read_only=True)

    class Meta:
        model = ApartmentReservation
        fields = [
            'id', 'user', 'apartment', 'reservation_number',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_amount', 'status', 'special_requests', 'payments',
            'cancellation_policy', 'created_at', 'updated_at'
        ]
        read_only_fields = ['reservation_number', 'created_at', 'updated_at']


class ApartmentReservationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de réservations d'appartements
    """
    class Meta:
        model = ApartmentReservation
        fields = [
            'apartment', 'check_in_date', 'check_out_date',
            'guest_name', 'guest_email', 'guest_phone', 'number_of_guests',
            'total_amount', 'special_requests'
        ]
    
    def create(self, validated_data):
        # Extraire les données spécifiques à l'appartement
        apartment = validated_data.pop('apartment')
        
        # Créer l'instance ApartmentReservation avec tous les champs nécessaires
        apartment_reservation = ApartmentReservation(
            apartment=apartment,
            **validated_data
        )
        apartment_reservation.save()
        return apartment_reservation 