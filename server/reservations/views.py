from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from .models import Reservation, HotelReservation, ApartmentReservation, Payment, CancellationPolicy
from .serializers import (
    ReservationSerializer, HotelReservationSerializer, ApartmentReservationSerializer,
    PaymentSerializer, CancellationPolicySerializer, ReservationCreateSerializer,
    HotelReservationCreateSerializer, ApartmentReservationCreateSerializer
)
from users.permissions import IsAdminUser, IsOwnerOrReadOnly
from hotels.models import Hotel, RoomType
from apartments.models import Apartment


class ReservationListView(generics.ListAPIView):
    """
    Liste des réservations (admin seulement)
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'check_in_date', 'check_out_date', 'user']
    search_fields = ['reservation_number', 'user__username', 'user__email']
    ordering_fields = ['created_at', 'check_in_date', 'total_amount']
    ordering = ['-created_at']

    def get_queryset(self):
        return Reservation.objects.all()


class ReservationDetailView(generics.RetrieveAPIView):
    """
    Détails d'une réservation
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


class ReservationCreateView(generics.CreateAPIView):
    """
    Créer une réservation (utilisateur connecté)
    """
    serializer_class = ReservationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationUpdateView(generics.UpdateAPIView):
    """
    Modifier une réservation (propriétaire ou admin seulement)
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


class ReservationCancelView(generics.UpdateAPIView):
    """
    Annuler une réservation
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'message': 'Réservation annulée avec succès'})


class ReservationDeleteView(generics.DestroyAPIView):
    """
    Supprimer une réservation (admin seulement)
    """
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    lookup_field = 'pk'


# Vues pour les réservations d'hôtels
class HotelReservationListView(generics.ListCreateAPIView):
    """
    Liste et création de réservations d'hôtels
    """
    serializer_class = HotelReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'hotel', 'room_type', 'check_in_date', 'check_out_date']
    search_fields = ['reservation_number', 'hotel__name', 'user__username']
    ordering_fields = ['created_at', 'check_in_date', 'total_amount']
    ordering = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return HotelReservation.objects.all()
        return HotelReservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'une réservation d'hôtel
    """
    queryset = HotelReservation.objects.all()
    serializer_class = HotelReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vues pour les réservations d'appartements
class ApartmentReservationListView(generics.ListCreateAPIView):
    """
    Liste et création de réservations d'appartements
    """
    serializer_class = ApartmentReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'apartment', 'check_in_date', 'check_out_date']
    search_fields = ['reservation_number', 'apartment__name', 'user__username']
    ordering_fields = ['created_at', 'check_in_date', 'total_amount']
    ordering = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return ApartmentReservation.objects.all()
        return ApartmentReservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApartmentReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'une réservation d'appartement
    """
    queryset = ApartmentReservation.objects.all()
    serializer_class = ApartmentReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vues pour les paiements
class PaymentListView(generics.ListCreateAPIView):
    """
    Liste et création de paiements
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'reservation']
    search_fields = ['transaction_id', 'reservation__reservation_number']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(reservation__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'un paiement
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vues pour les politiques d'annulation
class CancellationPolicyListView(generics.ListCreateAPIView):
    """
    Liste et création de politiques d'annulation
    """
    queryset = CancellationPolicy.objects.all()
    serializer_class = CancellationPolicySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'free_cancellation_hours']
    search_fields = ['name', 'description']
    ordering_fields = ['free_cancellation_hours', 'created_at']
    ordering = ['-created_at']


class CancellationPolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'une politique d'annulation
    """
    queryset = CancellationPolicy.objects.all()
    serializer_class = CancellationPolicySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    lookup_field = 'pk'


# Vues pour le dashboard et les statistiques
class DashboardStatsView(APIView):
    """
    Statistiques générales du dashboard (admin seulement)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_reservations = Reservation.objects.count()
        active_reservations = Reservation.objects.filter(status='confirmed').count()
        cancelled_reservations = Reservation.objects.filter(status='cancelled').count()
        total_revenue = Reservation.objects.filter(status='confirmed').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        stats = {
            'total_reservations': total_reservations,
            'active_reservations': active_reservations,
            'cancelled_reservations': cancelled_reservations,
            'total_revenue': float(total_revenue),
            'reservations_by_status': {
                'confirmed': Reservation.objects.filter(status='confirmed').count(),
                'pending': Reservation.objects.filter(status='pending').count(),
                'cancelled': cancelled_reservations,
                'completed': Reservation.objects.filter(status='completed').count(),
            }
        }
        
        return Response(stats)


class ReservationStatsView(APIView):
    """
    Statistiques des réservations (admin seulement)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Réservations par mois
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        months_ago = now - timedelta(days=365)
        
        monthly_reservations = Reservation.objects.filter(
            created_at__gte=months_ago
        ).extra(
            select={'month': "EXTRACT(month FROM created_at)"}
        ).values('month').annotate(
            count=models.Count('id')
        ).order_by('month')
        
        # Réservations par type
        hotel_reservations = HotelReservation.objects.count()
        apartment_reservations = ApartmentReservation.objects.count()
        
        stats = {
            'monthly_reservations': list(monthly_reservations),
            'hotel_reservations': hotel_reservations,
            'apartment_reservations': apartment_reservations,
            'total_reservations': hotel_reservations + apartment_reservations,
        }
        
        return Response(stats)


class RevenueStatsView(APIView):
    """
    Statistiques des revenus (admin seulement)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_revenue = Reservation.objects.filter(status='confirmed').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        hotel_revenue = HotelReservation.objects.filter(status='confirmed').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        apartment_revenue = ApartmentReservation.objects.filter(status='confirmed').aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        
        stats = {
            'total_revenue': float(total_revenue),
            'hotel_revenue': float(hotel_revenue),
            'apartment_revenue': float(apartment_revenue),
            'average_reservation_value': float(total_revenue / Reservation.objects.filter(status='confirmed').count()) if Reservation.objects.filter(status='confirmed').count() > 0 else 0,
        }
        
        return Response(stats)


class UserStatsView(APIView):
    """
    Statistiques des utilisateurs (admin seulement)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        from users.models import User
        
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        users_with_reservations = User.objects.filter(reservations__isnull=False).distinct().count()
        
        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'users_with_reservations': users_with_reservations,
            'users_by_type': {
                'clients': User.objects.filter(user_type='client').count(),
                'admins': User.objects.filter(user_type='admin').count(),
            }
        }
        
        return Response(stats)
