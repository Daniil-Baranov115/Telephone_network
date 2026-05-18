from django.test import TestCase
from billing.models import Client, Tariff
from decimal import Decimal


class ClientModelTest(TestCase):

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

    def test_client_initial_balance(self):
        self.assertEqual(self.client.get_balance(), 100.0)

    def test_client_add_balance(self):
        self.client.add_balance(50.0)
        self.assertEqual(float(self.client.balance), 150.0)

    def test_client_deduct_balance_success(self):
        result = self.client.deduct_balance(30.0)
        self.assertTrue(result)
        self.assertEqual(float(self.client.balance), 70.0)

    def test_client_deduct_balance_insufficient(self):
        result = self.client.deduct_balance(200.0)
        self.assertFalse(result)
        self.assertEqual(float(self.client.balance), 100.0)
