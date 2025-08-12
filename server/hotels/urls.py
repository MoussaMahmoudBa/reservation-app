from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    # Hotels RESTful combined
    path('', views.HotelListCreateView.as_view(), name='hotel_list_create'),
    path('<int:pk>/', views.HotelRetrieveUpdateDestroyView.as_view(), name='hotel_rud'),
    
    # Hotel Reviews - Ajout de l'endpoint racine pour les reviews
    path('reviews/', views.HotelReviewListView.as_view(), name='hotel_review_list_root'),
    path('<int:hotel_id>/reviews/', views.HotelReviewListView.as_view(), name='hotel_review_list'),
    path('<int:hotel_id>/reviews/create/', views.HotelReviewCreateView.as_view(), name='hotel_review_create'),
    path('reviews/<int:pk>/', views.HotelReviewDetailView.as_view(), name='hotel_review_detail'),
    path('reviews/<int:pk>/update/', views.HotelReviewUpdateView.as_view(), name='hotel_review_update'),
    path('reviews/<int:pk>/delete/', views.HotelReviewDeleteView.as_view(), name='hotel_review_delete'),
    
    # Room Types
    path('room-types/', views.RoomTypeListView.as_view(), name='room_type_list'),
    path('room-types/<int:pk>/', views.RoomTypeDetailView.as_view(), name='room_type_detail'),
    path('room-types/create/', views.RoomTypeCreateView.as_view(), name='room_type_create'),
    path('room-types/<int:pk>/update/', views.RoomTypeUpdateView.as_view(), name='room_type_update'),
    path('room-types/<int:pk>/delete/', views.RoomTypeDeleteView.as_view(), name='room_type_delete'),
    
    # Hotel Images
    path('images/', views.HotelImageListView.as_view(), name='hotel_image_list'),
    path('images/<int:pk>/', views.HotelImageDetailView.as_view(), name='hotel_image_detail'),
    path('images/create/', views.HotelImageCreateView.as_view(), name='hotel_image_create'),
    path('images/<int:pk>/update/', views.HotelImageUpdateView.as_view(), name='hotel_image_update'),
    path('images/<int:pk>/delete/', views.HotelImageDeleteView.as_view(), name='hotel_image_delete'),
    
    # Hotel-specific images
    path('<int:hotel_id>/images/', views.HotelImageCreateView.as_view(), name='hotel_image_create_specific'),
    
    # Search
    path('search/', views.HotelSearchView.as_view(), name='hotel_search'),
    
    # Upload
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('upload-media/', views.upload_media, name='upload_media'),
] 