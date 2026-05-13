from decimal import Decimal
from billing.services.tariff_strategy import DynamicTariffStrategy
from billing.models import Call, Device
from django.utils import timezone

class BillingService:
    def __init__(self, client_repo, device_repo):
        self.client_repo = client_repo
        self.device_repo = device_repo

    def process_call(self, from_device_id: int, to_device_id: int, duration_sec: int):
        from_device = self.device_repo.get_device(from_device_id)
        if not from_device:
            raise ValueError("Device not found")

        client = self.client_repo.get_client_by_device_id(from_device_id)
        tariff_strategy = DynamicTariffStrategy(client.tariff)
        duration_min = duration_sec / 60.0
        cost = tariff_strategy.calculate_cost(duration_min)

        if client.balance >= Decimal(str(cost)):
            client.balance -= Decimal(str(cost))
            self.client_repo.update_balance(client.id, client.balance)
            Call.objects.create(
                start_time=timezone.now(),
                duration_sec=duration_sec,
                cost=cost,
                from_device_id=from_device_id,
                to_device_id=to_device_id
            )
            return {"success": True, "cost": cost, "new_balance": client.balance}
        else:
            return {"success": False, "error": "Insufficient balance"}

    def get_client_balance(self, client_id: int):
        client = self.client_repo.get_client(client_id)
        return client.balance