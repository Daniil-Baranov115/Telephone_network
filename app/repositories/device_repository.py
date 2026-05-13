from abc import ABC, Abstractmethod

class DeviceRopository(ABC):
    @Abstractmethod
    def get_device(self, device_id: int):
        pass
    
    
    @Abstractmethod
    # возвращает все звонки в системе
    def deg_device_by_client(self, client_id: int):
        pass
    
    
    
    
    




