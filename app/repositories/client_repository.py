from abc import ABC, abstractmethod 

class ClientRepository:
    @abstractmethod
    def get_client(self, client_id: int):
        pass

    @abstractmethod
    def update_balance(self, client_id: int, amount: float) -> None:
        pass
    
    @abstractmethod
    # находит клиента по ID устройству
    def get_client_by_device_id(self, device_id: int):
        pass
