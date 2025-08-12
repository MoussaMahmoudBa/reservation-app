from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # Reservations
    path('', views.ReservationListView.as_view(), name='reservation_list'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/cancel/', views.ReservationCancelView.as_view(), name='reservation_cancel'),
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    
    # Hotel Reservations
    path('hotels/', views.HotelReservationListView.as_view(), name='hotel_reservation_list'),
    # Frontend alias
    path('hotel/', views.HotelReservationListView.as_view(), name='hotel_reservation_create'),
    path('hotels/<int:pk>/', views.HotelReservationDetailView.as_view(), name='hotel_reservation_detail'),
    
    # Apartment Reservations
    path('apartments/', views.ApartmentReservationListView.as_view(), name='apartment_reservation_list'),
    # Frontend alias
    path('apartment/', views.ApartmentReservationListView.as_view(), name='apartment_reservation_create'),
    path('apartments/<int:pk>/', views.ApartmentReservationDetailView.as_view(), name='apartment_reservation_detail'),
    
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    
    # Cancellation Policies
    path('cancellation-policies/', views.CancellationPolicyListView.as_view(), name='cancellation_policy_list'),
    path('cancellation-policies/<int:pk>/', views.CancellationPolicyDetailView.as_view(), name='cancellation_policy_detail'),
    
    # Dashboard (admin)
    path('stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
    path('stats/reservations/', views.ReservationStatsView.as_view(), name='reservation_stats'),
    path('stats/revenue/', views.RevenueStatsView.as_view(), name='revenue_stats'),
    path('stats/users/', views.UserStatsView.as_view(), name='user_stats'),
] 