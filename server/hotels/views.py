from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hotel, HotelImage, RoomType, HotelReview
from .serializers import (
    HotelSerializer,
    HotelCreateSerializer,
    HotelUpdateSerializer,
    HotelImageSerializer,
    RoomTypeSerializer,
    HotelReviewSerializer,
)
from users.permissions import IsAdminUser, IsOwnerOrReadOnly
import cloudinary
import cloudinary.uploader
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser


class HotelListView(generics.ListAPIView):
    """Vue pour lister les hôtels"""
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stars', 'city', 'wifi', 'air_conditioning', 'pool', 'gym', 'spa']
    search_fields = ['name', 'address', 'city', 'description']
    ordering_fields = ['rating', 'stars', 'price_per_night', 'created_at']
    ordering = ['-rating', '-stars']


class HotelListCreateView(generics.ListCreateAPIView):
    """Liste (GET) et création (POST) d'hôtels selon les attentes REST du frontend"""
    queryset = Hotel.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stars', 'city', 'wifi', 'air_conditioning', 'pool', 'gym', 'spa']
    search_fields = ['name', 'address', 'city', 'description']
    ordering_fields = ['rating', 'stars', 'created_at']
    ordering = ['-rating', '-stars']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            print("DEBUG: Using HotelCreateSerializer for POST request")
            return HotelCreateSerializer
        return HotelSerializer

    def perform_create(self, serializer):
        print("DEBUG: perform_create called")
        print(f"DEBUG: validated_data: {serializer.validated_data}")
        print(f"DEBUG: request.data: {self.request.data}")
        # Utiliser la méthode create du sérialiseur qui gère les images
        serializer.save()


class HotelDetailView(generics.RetrieveAPIView):
    """Vue pour récupérer les détails d'un hôtel"""
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]


class HotelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Détail (GET), mise à jour (PUT/PATCH) et suppression (DELETE) REST"""
    queryset = Hotel.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return HotelUpdateSerializer
        return HotelSerializer

    def destroy(self, request, *args, **kwargs):
        hotel = self.get_object()
        hotel.is_active = False
        hotel.save()
        return Response({'message': 'Hôtel désactivé avec succès'})


class HotelCreateView(generics.CreateAPIView):
    """Vue pour créer un hôtel (admin)"""
    serializer_class = HotelCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour un hôtel (admin)"""
    queryset = Hotel.objects.all()
    serializer_class = HotelUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer un hôtel (admin)"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        hotel = self.get_object()
        hotel.is_active = False
        hotel.save()
        return Response({
            'message': 'Hôtel désactivé avec succès'
        }, status=status.HTTP_200_OK)


class HotelReviewListView(generics.ListCreateAPIView):
    """Vue pour lister et créer des avis d'hôtel"""
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Si hotel_id est fourni, filtrer par hôtel, sinon retourner toutes les reviews
        hotel_id = self.kwargs.get('hotel_id')
        if hotel_id:
            return HotelReview.objects.filter(hotel_id=hotel_id)
        return HotelReview.objects.all()

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        if hotel_id:
            serializer.save(
                hotel_id=hotel_id,
                user=self.request.user
            )
        else:
            serializer.save(user=self.request.user)


class HotelReviewCreateView(generics.CreateAPIView):
    """Vue pour créer un avis d'hôtel"""
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            hotel_id=self.kwargs['hotel_id'],
            user=self.request.user
        )


class HotelReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, mettre à jour et supprimer un avis d'hôtel"""
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class HotelReviewUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour un avis d'hôtel"""
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class HotelReviewDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer un avis d'hôtel"""
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RoomTypeListView(generics.ListAPIView):
    """Vue pour lister les types de chambres"""
    queryset = RoomType.objects.filter(is_available=True)
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hotel', 'category', 'is_available']
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['price_per_night']


class RoomTypeDetailView(generics.RetrieveAPIView):
    """Vue pour récupérer les détails d'un type de chambre"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.AllowAny]


class RoomTypeCreateView(generics.CreateAPIView):
    """Vue pour créer un type de chambre (admin)"""
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class RoomTypeUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour un type de chambre (admin)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class RoomTypeDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer un type de chambre (admin)"""
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelImageListView(generics.ListAPIView):
    """Vue pour lister les images d'hôtel"""
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hotel', 'is_primary']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']


class HotelImageDetailView(generics.RetrieveAPIView):
    """Vue pour récupérer les détails d'une image d'hôtel"""
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.AllowAny]


class HotelImageCreateView(generics.CreateAPIView):
    """Vue pour créer une image d'hôtel (admin)"""
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelImageUpdateView(generics.UpdateAPIView):
    """Vue pour mettre à jour une image d'hôtel (admin)"""
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelImageDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer une image d'hôtel (admin)"""
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HotelSearchView(APIView):
    """Vue pour la recherche d'hôtels"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        hotels = Hotel.objects.filter(
            is_active=True,
            name__icontains=query
        ) | Hotel.objects.filter(
            is_active=True,
            city__icontains=query
        )
        
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


class FileUploadView(APIView):
    """Vue pour l'upload de fichiers"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Ici vous pouvez implémenter la logique d'upload
        # vers Cloudinary ou un autre service
        return Response({
            'message': 'Upload de fichier implémenté'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """
    Upload une image vers Cloudinary
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
            folder="reservation/hotels",
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
def upload_media(request):
    """
    Upload une image ou vidéo vers Cloudinary
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

        # Configuration Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret']
        )

        # Déterminer le dossier selon le type
        folder = f"reservation/hotels/{media_type}s"

        # Upload vers Cloudinary
        upload_result = cloudinary.uploader.upload(
            media_file,
            folder=folder,
            resource_type="auto",
            allowed_formats=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'wmv'],
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'fill'} if media_type == 'image' else {},
                {'quality': 'auto'} if media_type == 'image' else {}
            ]
        )

        return Response({
            'success': True,
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'type': media_type,
            'format': upload_result.get('format', ''),
            'duration': upload_result.get('duration', 0) if media_type == 'video' else None
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f"Erreur lors de l'upload: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([permissions.AllowAny])  # Permettre l'accès sans authentification
def unified_upload(request):
    """
    Endpoint unique d'upload conforme au client:
    - Champ fichier: 'file'
    - Paramètre 'type': 'hotel' | 'apartment' | 'profile'
    """
    try:
        # Vérification du fichier
        if 'file' not in request.FILES:
            return Response({
                'error': 'Aucun fichier fourni',
                'details': 'Le champ "file" est requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        media_type = request.POST.get('type', 'hotel')

        # Validation du type de fichier
        allowed_image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        allowed_video_types = ['video/mp4', 'video/mov', 'video/avi', 'video/wmv', 'video/quicktime']
        allowed_types = allowed_image_types + allowed_video_types
        
        if uploaded_file.content_type not in allowed_types:
            return Response({
                'error': 'Type de fichier non supporté',
                'details': f'Types supportés: {", ".join(allowed_types)}',
                'received_type': uploaded_file.content_type
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de la taille du fichier (max 50MB pour les vidéos, 10MB pour les images)
        is_video = uploaded_file.content_type.startswith('video/')
        max_size = 50 * 1024 * 1024 if is_video else 10 * 1024 * 1024  # 50MB pour vidéos, 10MB pour images
        
        if uploaded_file.size > max_size:
            max_size_mb = 50 if is_video else 10
            return Response({
                'error': 'Fichier trop volumineux',
                'details': f'Taille maximale: {max_size_mb}MB, reçue: {uploaded_file.size / (1024*1024):.1f}MB'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier que les credentials Cloudinary sont configurés
        if not all([
            settings.CLOUDINARY.get('cloud_name'),
            settings.CLOUDINARY.get('api_key'),
            settings.CLOUDINARY.get('api_secret')
        ]):
            return Response({
                'error': 'Configuration Cloudinary manquante',
                'details': 'Contactez l\'administrateur'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cloudinary.config(
            cloud_name=settings.CLOUDINARY['cloud_name'],
            api_key=settings.CLOUDINARY['api_key'],
            api_secret=settings.CLOUDINARY['api_secret']
        )

        folder_map = {
            'hotel': 'reservation/hotels',
            'apartment': 'reservation/apartments',
            'profile': 'reservation/profiles',
        }
        folder = folder_map.get(media_type, 'reservation/misc')

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

        # Upload vers Cloudinary avec gestion d'erreur améliorée
        upload_result = cloudinary.uploader.upload(
            uploaded_file,
            **upload_options
        )

        # Optionnel: si 'profile' => enregistrer l'URL sur l'utilisateur connecté
        if media_type == 'profile' and request.user and request.user.is_authenticated:
            user = request.user
            # Si le modèle a un champ d'URL, le renseigner
            if hasattr(user, 'profile_picture_url'):
                user.profile_picture_url = upload_result['secure_url']
                user.save(update_fields=['profile_picture_url'])

        return Response({
            'success': True,
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'type': media_type,
            'format': upload_result.get('format', ''),
            'duration': upload_result.get('duration', 0) if upload_result.get('resource_type') == 'video' else None,
            'size': upload_result.get('bytes', 0),
            'width': upload_result.get('width', 0),
            'height': upload_result.get('height', 0)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Erreur upload Cloudinary: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': 'Erreur lors de l\'upload',
            'details': str(e),
            'type': 'upload_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
