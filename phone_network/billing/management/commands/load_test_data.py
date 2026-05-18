from django.core.management.base import BaseCommand
from billing.models import Tariff, Client, Device, Call
from datetime import datetime, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Загружает тестовые данные'

    def handle(self, *args, **options):
        # Создание тарифов
        tariffs_data = [
            {'name': 'Мобильный', 'price_per_minute': 1.0},
            {'name': 'Домашний', 'price_per_minute': 0.5},
            {'name': 'Премиум', 'price_per_minute': 1.5},
        ]

        tariffs = {}
        for tariff_data in tariffs_data:
            tariff, _ = Tariff.objects.get_or_create(
                name=tariff_data['name'], defaults=tariff_data)
            tariffs[tariff_data['name']] = tariff

        # Создание клиентов
        clients_data = [
            {
                'username': 'admin',
                'name': 'Администратор Системы',
                'balance': 10000.0,
                'tariff': tariffs['Премиум'],
                'password': '115',
                'is_admin': True
            },
            {
                'username': 'ivanov',
                'name': 'Иван Иванов',
                'balance': 500.0,
                'tariff': tariffs['Мобильный'],
                'password': '123',
                'is_admin': False
            },
            {
                'username': 'petrov',
                'name': 'Петр Петров',
                'balance': 300.0,
                'tariff': tariffs['Домашний'],
                'password': '123',
                'is_admin': False
            },
            {
                'username': 'sidorova',
                'name': 'Анна Сидорова',
                'balance': 750.0,
                'tariff': tariffs['Премиум'],
                'password': '123',
                'is_admin': False
            },
            {
                'username': 'kozlov',
                'name': 'Михаил Козлов',
                'balance': 200.0,
                'tariff': tariffs['Мобильный'],
                'password': '123',
                'is_admin': False
            },
        ]

        clients = {}
        for client_data in clients_data:
            client, _ = Client.objects.get_or_create(
                username=client_data['username'],
                defaults=client_data
            )
            clients[client_data['username']] = client

        # Создание устройств
        devices_data = [
            {'phone_number': '+7 (999) 111-22-33',
             'device_type': 'mobile', 'client': clients['admin']},
            {'phone_number': '+7 (999) 222-33-44',
             'device_type': 'home', 'client': clients['admin']},
            {'phone_number': '+7 (999) 123-45-67',
             'device_type': 'mobile', 'client': clients['ivanov']},
            {'phone_number': '+7 (812) 555-12-34',
             'device_type': 'home', 'client': clients['ivanov']},
            {'phone_number': '+7 (999) 234-56-78',
             'device_type': 'mobile', 'client': clients['petrov']},
            {'phone_number': '+7 (812) 666-23-45', 'device_type': 'home',
             'client': clients['sidorova']},
            {'phone_number': '+7 (999) 345-67-89',
             'device_type': 'mobile', 'client': clients['kozlov']},
        ]

        for device_data in devices_data:
            Device.objects.get_or_create(
                phone_number=device_data['phone_number'],
                defaults=device_data
            )

        # Создание тестовых звонков
        devices = {d.phone_number: d for d in Device.objects.all()}

        calls_data = [
            ('+7 (999) 123-45-67', '+7 (999) 234-56-78', 5, 2),
            ('+7 (999) 123-45-67', '+7 (812) 666-23-45', 10, 1),
            ('+7 (999) 234-56-78', '+7 (999) 111-22-33', 8, 3),
            ('+7 (812) 555-12-34', '+7 (999) 345-67-89', 15, 1),
            ('+7 (999) 345-67-89', '+7 (999) 123-45-67', 3, 2),
            ('+7 (812) 666-23-45', '+7 (812) 555-12-34', 20, 5),
        ]

        for from_num, to_num, duration, days_ago in calls_data:
            if from_num in devices and to_num in devices:
                client = devices[from_num].client
                tariff_strategy = None
                for t in tariffs.values():
                    if t.name == client.tariff.name:
                        cost = duration * float(t.price_per_minute)
                        break

                Call.objects.create(
                    start_time=datetime.now() - timedelta(days=days_ago),
                    duration_sec=duration * 60,
                    cost=cost,
                    from_device=devices[from_num],
                    to_device=devices[to_num]
                )

                # Списываем средства за звонок
                if client.balance >= cost:
                    client.balance -= cost
                    client.save()

        self.stdout.write(self.style.SUCCESS(
            '✅ Тестовые данные успешно загружены!'))
        self.stdout.write(self.style.SUCCESS(
            '📞 Администратор: Логин "admin", Пароль "115"'))
        self.stdout.write(self.style.SUCCESS(
            '👤 Пользователи: Логин "ivanov", "petrov", "sidorova", "kozlov", Пароль "123"'))
