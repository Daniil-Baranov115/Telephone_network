from django.test import TestCase
from billing.models import Client, Tariff, Device


class ClientTestCase(TestCase):
    def setUp(self):
        self.tariff = Tariff.objects.create(name="Test", price_per_minute=1.0)
        self.client = Client.objects.create(
            name="Test", balance=100, tariff=self.tariff)

    def test_client_initial_balance(self):
        self.assertEqual(self.client.get_balance(), 100)

    def test_client_add_balance(self):
        self.client.add_balance(50)
        self.assertEqual(self.client.balance, 150)
