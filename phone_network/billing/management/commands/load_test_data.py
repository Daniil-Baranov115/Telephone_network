from django.core.management.base import BaseCommand
from billing.models import Tariff, Client, Device


class Command(BaseCommand):
    help = 'Загружает тестовые данные'

    def handle(self, *args, **options):
        # Создание тарифов
        tariffs = [
            {'name': 'Мобильный', 'price_per_minute': 1.0},
            {'name': 'Домашний', 'price_per_minute': 0.5},
            {'name': 'Премиум', 'price_per_minute': 1.5},
        ]

        for tariff_data in tariffs:
            Tariff.objects.get_or_create(
                name=tariff_data['name'], defaults=tariff_data)

        # Создание клиентов
        mobile_tariff = Tariff.objects.get(name='Мобильный')
        client1, _ = Client.objects.get_or_create(
            username='ivan',
            defaults={
                'name': 'Иван Петров',
                'balance': 100.0,
                'tariff': mobile_tariff,
                'password': '123',
                'is_admin': False
            }
        )

        client2, _ = Client.objects.get_or_create(
            username='admin',
            defaults={
                'name': 'Администратор',
                'balance': 1000.0,
                'tariff': mobile_tariff,
                'password': 'admin123',
                'is_admin': True
            }
        )

        # Создание устройств
        Device.objects.get_or_create(
            phone_number='+79991234567',
            defaults={
                'device_type': 'mobile',
                'client': client1
            }
        )

        Device.objects.get_or_create(
            phone_number='+79990001111',
            defaults={
                'device_type': 'mobile',
                'client': client2
            }
        )

        self.stdout.write(self.style.SUCCESS(
            'Тестовые данные успешно загружены!'))
