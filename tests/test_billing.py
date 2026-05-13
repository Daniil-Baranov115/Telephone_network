import pytest
from app.services.billing_service import BillingService
from app.models.tariffs import MobileTariff, HomeTariff

# Мок-репозитории


class MockClientRepo:
    def __init__(self):
        self.clients = {1: {"id": 1, "balance": 100.0, "tariff_id": 1}}

    def get_client(self, client_id):
        return self.clients.get(client_id)

    def update_balance(self, client_id, amount):
        if client_id in self.clients:
            self.clients[client_id]["balance"] = amount

    def get_clients_by_device_id(self, device_id):
        if device_id == 100:
            return {"id": 1, "balance": 100.0, "tariff_id": 1}

        return None

class MockDeviceRepo:
    def get_device(self, device_id):
        if device_id == 100:
            return {"id": 100, "client_id": 1}
                    
        return None
    
    
class MockCallRepo:
    def save_call(self, call):
        pass
 
 
def test_process_call_success():
    """Тест 1: Успешный звонок с мобильного тарифа"""
    client_repo = MockClientRepo()
    device_repo = MockDeviceRepo()
    call_repo = MockCallRepo()
    
    service = BillingService(client_repo, device_repo, call_repo)
    service.set_tariff_strategy(MobileTariff())
    
   
    result = service.process_call(from_device_id=100, duration_minutes=5)
    assert result == True


def test_process_call_insufficient_balance():
    """Тест 2: Недостаточно средств на балансе"""
    client_repo = MockClientRepo()
    device_repo = MockDeviceRepo()
    call_repo = MockCallRepo()
    
    service = BillingService(client_repo, device_repo, call_repo)
    service.set_tariff_strategy(MobileTariff())
    
    # Баланс 100 руб, звонок 200 минут по 1 руб = 200 руб
    # Должен вернуть False
    result = service.process_call(from_device_id=100, duration_minutes=200)
    assert result == False


def test_process_call_device_not_found():
    """Тест 3: Устройство не найдено"""
    client_repo = MockClientRepo()
    device_repo = MockDeviceRepo()
    call_repo = MockCallRepo()
    
    service = BillingService(client_repo, device_repo, call_repo)
    service.set_tariff_strategy(MobileTariff())
    
    # Устройства с ID 999 не существует
    with pytest.raises(Exception):
        service.process_call(from_device_id=999, duration_minutes=5)   
     

def test_get_client_balance():
    """Тест 4: Получение баланса клиента"""
    client_repo = MockClientRepo()
    device_repo = MockDeviceRepo()
    call_repo = MockCallRepo()
    
    service = BillingService(client_repo, device_repo, call_repo)
    
    balance = service.get_client_balance(client_id=1)
    assert balance == 100.0


