from django.utils import timezone
from billing.models import Client, Device, Call
from .tariff_strategy import get_tariff_strategy


class BillingService:

    @staticmethod
    def process_call(from_device_id: int, to_phone_number: str, duration_minutes: int):
        """Обработка звонка"""
        try:
            from_device = Device.objects.get(id=from_device_id)
            client = from_device.client

            try:
                to_device = Device.objects.get(phone_number=to_phone_number)
            except Device.DoesNotExist:
                return {"success": False, "error": "Номер получателя не найден"}

            tariff_strategy = get_tariff_strategy(
                client.tariff.name if client.tariff else "Мобильный")
            cost = tariff_strategy.calculate_cost(duration_minutes)

            if client.balance >= cost:
                client.balance -= cost
                client.save(update_fields=['balance'])

                Call.objects.create(
                    start_time=timezone.now(),
                    duration_sec=duration_minutes * 60,
                    cost=cost,
                    from_device=from_device,
                    to_device=to_device
                )

                return {
                    "success": True,
                    "cost": cost,
                    "new_balance": client.balance,
                    "message": f"Звонок совершен. Стоимость: {cost} руб"
                }
            else:
                return {
                    "success": False,
                    "error": f"Недостаточно средств. Требуется: {cost} руб, доступно: {client.balance} руб"
                }

        except Device.DoesNotExist:
            return {"success": False, "error": "Устройство не найдено"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_client_balance(client_id: int) -> float:
        try:
            client = Client.objects.get(id=client_id)
            return client.balance
        except Client.DoesNotExist:
            return 0.0
