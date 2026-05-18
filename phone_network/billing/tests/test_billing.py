from django.test import TestCase
from billing.models import Client, Tariff, Device
from billing.services.billing_service import BillingService


class BillingServiceTest(TestCase):

    def setUp(self):
        self.tariff = Tariff.objects.create(
            name="Мобильный", price_per_minute=1.0)
        self.client = Client.objects.create(
            name="Тестовый Клиент",
            balance=100.0,
            tariff=self.tariff,
            username="testuser",
            password="password"
        )
        self.device = Device.objects.create(
            phone_number="+79991234567",
            device_type="mobile",
            client=self.client
        )
        self.target_device = Device.objects.create(
            phone_number="+79998765432",
            device_type="mobile",
            client=self.client
        )

    def test_process_call_success(self):
        result = BillingService.process_call(self.device.id, "+79998765432", 5)
        self.assertTrue(result['success'])
        self.assertEqual(result['cost'], 5.0)

    def test_process_call_insufficient_balance(self):
        self.client.balance = 3.0
        self.client.save()
        result = BillingService.process_call(self.device.id, "+79998765432", 5)
        self.assertFalse(result['success'])
        self.assertIn("Недостаточно средств", result['error'])

    def test_process_call_device_not_found(self):
        result = BillingService.process_call(999, "+79998765432", 5)
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Устройство не найдено")

    def test_get_client_balance(self):
        balance = BillingService.get_client_balance(self.client.id)
        self.assertEqual(balance, 100.0)
