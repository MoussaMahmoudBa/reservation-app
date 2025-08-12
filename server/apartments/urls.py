from django.urls import path
from . import views

app_name = 'apartments'

urlpatterns = [
    # Apartments RESTful combined
    path('', views.ApartmentListCreateView.as_view(), name='apartment_list_create'),
    path('<int:pk>/', views.ApartmentRetrieveUpdateDestroyView.as_view(), name='apartment_rud'),
    
    # Apartment Reviews
    path('<int:apartment_id>/reviews/', views.ApartmentReviewListView.as_view(), name='apartment_review_list'),
    path('reviews/<int:pk>/', views.ApartmentReviewDetailView.as_view(), name='apartment_review_detail'),
    
    # Apartment Images
    path('<int:apartment_id>/images/', views.ApartmentImageListView.as_view(), name='apartment_image_list'),
    path('images/<int:pk>/', views.ApartmentImageDetailView.as_view(), name='apartment_image_detail'),
    
    # Apartment Availability
    path('<int:apartment_id>/availability/', views.ApartmentAvailabilityListView.as_view(), name='apartment_availability_list'),
    path('availability/<int:pk>/', views.ApartmentAvailabilityDetailView.as_view(), name='apartment_availability_detail'),
    
    # Search and Stats
    path('search/', views.ApartmentSearchView.as_view(), name='apartment_search'),
    
    # Upload
    path('upload-image/', views.upload_apartment_image, name='upload_apartment_image'),
    path('upload-media/', views.upload_apartment_media, name='upload_apartment_media'),
    path('stats/', views.ApartmentStatsView.as_view(), name='apartment_stats'),
] 