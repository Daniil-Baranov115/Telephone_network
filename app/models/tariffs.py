from abc import ABC, abstractmethod

class TariffStrategy:
    @abstractmethod
    def calculate_cost(self, duration_minutes: int) -> float:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
   
    
class MobileTariff(TariffStrategy):
    
    def calculate_cost(self, duration_minutes: int) -> float:
        pass
    
class HomeTariff(TariffStrategy):
    
    def calculate_cost(self, duration_minutes: int) -> float:
        pass
    
    def get_name(self) -> str:
        pass
    
class PremiumTariff(TariffStrategy):
    
    def calculate_cost(self, duration_minutes: int) -> float:
        pass
    
    def get_name(self) -> str:
        pass




