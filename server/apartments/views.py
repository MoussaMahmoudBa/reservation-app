from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Apartment, ApartmentImage, ApartmentReview, ApartmentAvailability
from .serializers import (
    ApartmentSerializer, ApartmentCreateSerializer, ApartmentUpdateSerializer,
    ApartmentImageSerializer, ApartmentReviewSerializer, ApartmentAvailabilitySerializer,
    ApartmentSearchSerializer, ApartmentStatsSerializer
)
from users.permissions import IsAdminUser, IsOwnerOrReadOnly
from django.db import models
import cloudinary
import cloudinary.uploader
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


class ApartmentListView(generics.ListAPIView):
    """
    Liste des appartements avec filtrage et recherche
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['apartment_type', 'property_type', 'bedrooms', 'bathrooms', 'price_per_night', 'city']
    search_fields = ['name', 'description', 'address', 'city']
    ordering_fields = ['price_per_night', 'rating', 'created_at', 'name']
    ordering = ['-created_at']


class ApartmentListCreateView(generics.ListCreateAPIView):
    queryset = Apartment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['apartment_type', 'property_type', 'bedrooms', 'bathrooms', 'price_per_night', 'city']
    search_fields = ['name', 'description', 'address', 'city']
    ordering_fields = ['price_per_night', 'rating', 'created_at', 'name']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ApartmentCreateSerializer
        return ApartmentSerializer

    def perform_create(self, serializer):
        # Utiliser la méthode create du sérialiseur qui gère les images
        serializer.save()


class ApartmentDetailView(generics.RetrieveAPIView):
    """
    Détails d'un appartement
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    lookup_field = 'pk'


class ApartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Apartment.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ApartmentUpdateSerializer
        return ApartmentSerializer


class ApartmentCreateView(generics.CreateAPIView):
    """
    Créer un nouvel appartement (admin seulement)
    """
    serializer_class = ApartmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApartmentUpdateView(generics.UpdateAPIView):
    """
    Modifier un appartement (propriétaire ou admin seulement)
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


class ApartmentDeleteView(generics.DestroyAPIView):
    """
    Supprimer un appartement (propriétaire ou admin seulement)
    """
    queryset = Apartment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    lookup_field = 'pk'


# Vues pour les images d'appartements
class ApartmentImageListView(generics.ListCreateAPIView):
    """
    Liste et création d'images pour un appartement
    """
    serializer_class = ApartmentImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return ApartmentImage.objects.filter(apartment_id=apartment_id)

    def perform_create(self, serializer):
        apartment_id = self.kwargs.get('apartment_id')
        serializer.save(apartment_id=apartment_id)


class ApartmentImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'une image d'appartement
    """
    queryset = ApartmentImage.objects.all()
    serializer_class = ApartmentImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vues pour les avis d'appartements
class ApartmentReviewListView(generics.ListCreateAPIView):
    """
    Liste et création d'avis pour un appartement
    """
    serializer_class = ApartmentReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return ApartmentReview.objects.filter(apartment_id=apartment_id)

    def perform_create(self, serializer):
        apartment_id = self.kwargs.get('apartment_id')
        apartment = Apartment.objects.get(id=apartment_id)
        
        # Vérifier si l'utilisateur a déjà un avis pour cet appartement
        existing_review = ApartmentReview.objects.filter(
            apartment=apartment,
            user=self.request.user
        ).first()
        
        if existing_review:
            # Mettre à jour l'avis existant
            existing_review.rating = serializer.validated_data['rating']
            existing_review.title = serializer.validated_data['title']
            existing_review.comment = serializer.validated_data['comment']
            existing_review.save()
            # Retourner l'avis mis à jour
            serializer.instance = existing_review
        else:
            # Créer un nouvel avis
            serializer.save(apartment=apartment, user=self.request.user)
        
        # Mettre à jour la note moyenne de l'appartement
        apartment.update_rating()


class ApartmentReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'un avis d'appartement
    """
    queryset = ApartmentReview.objects.all()
    serializer_class = ApartmentReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vues pour la disponibilité des appartements
class ApartmentAvailabilityListView(generics.ListCreateAPIView):
    """
    Liste et création de disponibilités pour un appartement
    """
    serializer_class = ApartmentAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return ApartmentAvailability.objects.filter(apartment_id=apartment_id)

    def perform_create(self, serializer):
        apartment_id = self.kwargs.get('apartment_id')
        serializer.save(apartment_id=apartment_id)


class ApartmentAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détails, modification et suppression d'une disponibilité d'appartement
    """
    queryset = ApartmentAvailability.objects.all()
    serializer_class = ApartmentAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'


# Vue de recherche avancée
class ApartmentSearchView(generics.ListAPIView):
    """
    Recherche avancée d'appartements
    """
    serializer_class = ApartmentSearchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['apartment_type', 'property_type', 'bedrooms', 'bathrooms', 'price_per_night', 'city']
    search_fields = ['name', 'description', 'address', 'city']
    ordering_fields = ['price_per_night', 'rating', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Apartment.objects.all()
        
        # Filtres supplémentaires
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        check_in = self.request.query_params.get('check_in')
        check_out = self.request.query_params.get('check_out')
        
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
        return queryset


# Vue pour les statistiques des appartements
class ApartmentStatsView(APIView):
    """
    Statistiques des appartements (admin seulement)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_apartments = Apartment.objects.count()
        active_apartments = Apartment.objects.filter(is_active=True).count()
        total_reviews = ApartmentReview.objects.count()
        avg_rating = Apartment.objects.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        
        stats = {
            'total_apartments': total_apartments,
            'active_apartments': active_apartments,
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
        }
        
        return Response(stats)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_apartment_image(request):
    """
    Upload une image d'appartement vers Cloudinary
    """
    try:
        # Vérifier si une image a été envoyée
        if 'image' not in request.FILES:
            return Response(
                {'error': 'Aucune image fournie'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Configuration Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret']
        )
        
        # Upload vers Cloudinary
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder="reservation/apartments",
            resource_type="auto"
        )
        
        return Response({
            'success': True,
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'upload: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_apartment_media(request):
    """
    Upload une image ou vidéo d'appartement vers Cloudinary
    """
    try:
        # Vérifier si un fichier a été envoyé
        if 'media' not in request.FILES:
            return Response(
                {'error': 'Aucun fichier fourni'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        media_file = request.FILES['media']
        media_type = request.POST.get('type', 'image')  # 'image' ou 'video'
        
        # Validation du type de fichier
        is_video = media_file.content_type.startswith('video/')
        
        # Vérification de la taille du fichier (max 50MB pour les vidéos, 10MB pour les images)
        max_size = 50 * 1024 * 1024 if is_video else 10 * 1024 * 1024
        
        if media_file.size > max_size:
            max_size_mb = 50 if is_video else 10
            return Response({
                'error': 'Fichier trop volumineux',
                'details': f'Taille maximale: {max_size_mb}MB, reçue: {media_file.size / (1024*1024):.1f}MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Configuration Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret']
        )
        
        # Déterminer le dossier selon le type
        folder = f"reservation/apartments/{media_type}s"
        
        # Configuration d'upload selon le type de fichier
        upload_options = {
            'folder': folder,
            'resource_type': 'video' if is_video else 'image',
            'allowed_formats': ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'avi', 'wmv', 'qt'] if is_video else ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        }

        # Ajouter des transformations pour les images seulement
        if not is_video:
            upload_options['transformation'] = [
                {'width': 800, 'height': 600, 'crop': 'fill'},
                {'quality': 'auto'}
            ]
        
        # Upload vers Cloudinary
        upload_result = cloudinary.uploader.upload(
            media_file,
            **upload_options
        )
        
        return Response({
            'success': True,
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'type': media_type,
            'format': upload_result.get('format', ''),
            'duration': upload_result.get('duration', 0) if is_video else None,
            'size': upload_result.get('bytes', 0),
            'width': upload_result.get('width', 0),
            'height': upload_result.get('height', 0)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Erreur upload Cloudinary: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Erreur lors de l\'upload: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
