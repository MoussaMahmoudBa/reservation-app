from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reservation, HotelReservation, ApartmentReservation, Payment, CancellationPolicy


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Interface d'administration pour les réservations"""
    
    list_display = ('reservation_number', 'user', 'check_in_date', 'check_out_date', 'status', 'payment_status', 'final_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'is_cancelled', 'created_at')
    search_fields = ('reservation_number', 'user__username', 'user__email', 'guest_name', 'guest_email')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('user', 'reservation_number', 'check_in_date', 'check_out_date')
        }),
        (_('Informations des voyageurs'), {
            'fields': ('guest_name', 'guest_email', 'guest_phone', 'number_of_guests', 'special_requests')
        }),
        (_('Prix et paiement'), {
            'fields': ('total_amount', 'tax_amount', 'discount_amount', 'final_amount')
        }),
        (_('Statuts'), {
            'fields': ('status', 'payment_status')
        }),
        (_('Annulation'), {
            'fields': ('is_cancelled', 'cancellation_reason', 'cancelled_at', 'cancelled_by'),
            'classes': ('collapse',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('reservation_number', 'final_amount', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'cancelled_by')


@admin.register(HotelReservation)
class HotelReservationAdmin(admin.ModelAdmin):
    """Interface d'administration pour les réservations d'hôtels"""
    
    list_display = ('reservation_number', 'user', 'hotel', 'room_type', 'check_in_date', 'check_out_date', 'status', 'final_amount')
    list_filter = ('status', 'payment_status', 'hotel', 'room_type', 'created_at')
    search_fields = ('reservation_number', 'user__username', 'hotel__name', 'room_type__name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('user', 'reservation_number', 'hotel', 'room_type', 'check_in_date', 'check_out_date')
        }),
        (_('Informations des voyageurs'), {
            'fields': ('guest_name', 'guest_email', 'guest_phone', 'number_of_guests', 'special_requests')
        }),
        (_('Prix et paiement'), {
            'fields': ('total_amount', 'tax_amount', 'discount_amount', 'final_amount')
        }),
        (_('Statuts'), {
            'fields': ('status', 'payment_status')
        }),
        (_('Annulation'), {
            'fields': ('is_cancelled', 'cancellation_reason', 'cancelled_at', 'cancelled_by'),
            'classes': ('collapse',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('reservation_number', 'final_amount', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'hotel', 'room_type', 'cancelled_by')


@admin.register(ApartmentReservation)
class ApartmentReservationAdmin(admin.ModelAdmin):
    """Interface d'administration pour les réservations d'appartements"""
    
    list_display = ('reservation_number', 'user', 'apartment', 'check_in_date', 'check_out_date', 'status', 'final_amount')
    list_filter = ('status', 'payment_status', 'apartment', 'created_at')
    search_fields = ('reservation_number', 'user__username', 'apartment__name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('user', 'reservation_number', 'apartment', 'check_in_date', 'check_out_date')
        }),
        (_('Informations des voyageurs'), {
            'fields': ('guest_name', 'guest_email', 'guest_phone', 'number_of_guests', 'special_requests')
        }),
        (_('Prix et paiement'), {
            'fields': ('total_amount', 'tax_amount', 'discount_amount', 'final_amount')
        }),
        (_('Statuts'), {
            'fields': ('status', 'payment_status')
        }),
        (_('Annulation'), {
            'fields': ('is_cancelled', 'cancellation_reason', 'cancelled_at', 'cancelled_by'),
            'classes': ('collapse',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('reservation_number', 'final_amount', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'apartment', 'cancelled_by')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Interface d'administration pour les paiements"""
    
    list_display = ('transaction_id', 'reservation', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'payment_gateway', 'created_at')
    search_fields = ('transaction_id', 'reservation__reservation_number', 'reservation__user__username')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('reservation', 'amount', 'payment_method', 'status')
        }),
        (_('Transaction'), {
            'fields': ('transaction_id', 'payment_gateway')
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at', 'processed_at')
        }),
        (_('Erreur'), {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reservation', 'reservation__user')


@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    """Interface d'administration pour les politiques d'annulation"""
    
    list_display = ('name', 'free_cancellation_hours', 'refund_percentage_24h', 'refund_percentage_48h', 'refund_percentage_72h', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Délais d\'annulation'), {
            'fields': ('free_cancellation_hours',)
        }),
        (_('Pourcentages de remboursement'), {
            'fields': ('refund_percentage_24h', 'refund_percentage_48h', 'refund_percentage_72h')
        }),
        (_('Métadonnées'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
