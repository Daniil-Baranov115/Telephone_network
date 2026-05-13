from abc import ABC, abstractmethod
from billing.models import Client, Device


class ClientRepository(ABC):
    @abstractmethod
    def get_client(self, client_id: int):
        pass

    @abstractmethod
    def update_balance(self, client_id: int, amount: float):
        pass

    @abstractmethod
    def get_client_by_device_id(self, device_id: int):
        pass


class DjangoClientRepository(ClientRepository):
    def get_client(self, client_id: int):
        return Client.objects.get(id=client_id)

    def update_balance(self, client_id: int, amount: float):
        client = self.get_client(client_id)
        client.balance = amount
        client.save()

    def get_client_by_device_id(self, device_id: int):
        device = Device.objects.get(id=device_id)
        return device.client


class DeviceRepository(ABC):
    @abstractmethod
    def get_device(self, device_id: int):
        pass

    @abstractmethod
    def get_devices_by_client(self, client_id: int):
        pass


class DjangoDeviceRepository(DeviceRepository):
    def get_device(self, device_id: int):
        return Device.objects.get(id=device_id)

    def get_devices_by_client(self, client_id: int):
        return Device.objects.filter(client_id=client_id)
