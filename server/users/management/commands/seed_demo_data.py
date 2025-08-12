import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from hotels.models import Hotel, RoomType, HotelImage
from apartments.models import Apartment, ApartmentImage


class Command(BaseCommand):
    help = "Seed de données démo: users, hotels, apartments"

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', help='Créer des utilisateurs démo')
        parser.add_argument('--hotels', action='store_true', help='Créer des hôtels démo')
        parser.add_argument('--apartments', action='store_true', help='Créer des appartements démo')
        parser.add_argument('--all', action='store_true', help='Tout créer')

    def handle(self, *args, **options):
        do_users = options['users'] or options['all']
        do_hotels = options['hotels'] or options['all']
        do_apartments = options['apartments'] or options['all']

        if do_users:
            self._seed_users()
        if do_hotels:
            self._seed_hotels()
        if do_apartments:
            self._seed_apartments()

        self.stdout.write(self.style.SUCCESS('Seed terminé'))

    def _seed_users(self):
        User = get_user_model()
        # Admin: idempotent via username
        admin_username = 'admin'
        admin_phone = '+22212345678'
        admin = User.objects.filter(username=admin_username).first()
        if not admin:
            admin = User.objects.create(
                username=admin_username,
                phone=admin_phone,
                first_name='Admin',
                last_name='User',
                user_type='admin',
                is_staff=True,
                is_superuser=True,
            )
            admin.set_password('admin1234')
            admin.save()
        else:
            # S'assurer que les attributs principaux sont corrects
            updated = False
            if not admin.is_superuser:
                admin.is_superuser = True; updated = True
            if not admin.is_staff:
                admin.is_staff = True; updated = True
            if admin.user_type != 'admin':
                admin.user_type = 'admin'; updated = True
            if not admin.phone:
                admin.phone = admin_phone; updated = True
            if updated:
                admin.save()

        # Clients simples: éviter les conflits sur username ET phone
        for i in range(1, 6):
            username = f'user{i}'
            phone = f'+2221020304{i}'
            if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
                continue
            user = User.objects.create(
                username=username,
                phone=phone,
                first_name=f'User{i}',
                last_name='Client',
                user_type='client',
            )
            user.set_password('pass1234')
            user.save()

    def _seed_hotels(self):
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not admin:
            return
        hotel_names = [
            'Hotel Sahara', 'Hotel Dune', 'Hotel Oasis', 'Hotel Atlantic', 'Hotel Khaima'
        ]
        for name in hotel_names:
            hotel, _ = Hotel.objects.get_or_create(
                name=name,
                defaults={
                    'description': 'Bel hôtel situé au coeur de la ville.',
                    'address': 'Centre-ville',
                    'city': 'Nouakchott',
                    'country': 'Mauritanie',
                    'phone': '+222 45 00 00 00',
                    'email': 'contact@example.com',
                    'stars': random.choice([3, 4, 5]),
                    'wifi': True,
                    'air_conditioning': True,
                    'parking': True,
                    'created_by': admin,
                }
            )
            # Room types
            for rt_name, cat in [('Standard', 'double'), ('Suite', 'suite'), ('Familiale', 'family')]:
                RoomType.objects.get_or_create(
                    hotel=hotel,
                    name=rt_name,
                    defaults={
                        'category': cat,
                        'description': f'Type {rt_name} confortable.',
                        'capacity': random.choice([2, 3, 4]),
                        'price_per_night': random.choice([3500, 5000, 7000]),
                        'discount_percentage': random.choice([0, 5, 10]),
                        'is_available': True,
                    }
                )

    def _seed_apartments(self):
        User = get_user_model()
        owner = User.objects.filter(user_type='client').first() or User.objects.first()
        if not owner:
            return
        apt_names = [
            'Studio Tevragh-Zeina', 'F4 Ksar', 'Appartement Centre', 'Penthouse Nord', 'Villa Sud'
        ]
        for name in apt_names:
            apt, _ = Apartment.objects.get_or_create(
                name=name,
                defaults={
                    'description': 'Logement bien équipé et bien situé.',
                    'address': 'Quartier populaire',
                    'city': 'Nouakchott',
                    'country': 'Mauritanie',
                    'apartment_type': random.choice(['studio', 'one_bedroom', 'two_bedroom']),
                    'property_type': random.choice(['apartment', 'house', 'studio']),
                    'bedrooms': random.choice([1, 2, 3]),
                    'bathrooms': random.choice([1, 2]),
                    'max_guests': random.choice([2, 4, 6]),
                    'price_per_night': random.choice([2500, 4000, 6000]),
                    'owner': owner,
                    'wifi': True,
                    'air_conditioning': True,
                    'is_active': True,
                }
            )
