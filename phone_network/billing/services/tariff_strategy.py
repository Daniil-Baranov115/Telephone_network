from abc import ABC, abstractmethod

class TariffStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, duration_minutes: int) -> float:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class MobileTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 1.0
    
    def get_name(self) -> str:
        return "Мобильный (1 руб/мин)"

class HomeTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 0.5
    
    def get_name(self) -> str:
        return "Домашний (0.5 руб/мин)"

class PremiumTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 1.5
    
    def get_name(self) -> str:
        return "Премиум (1.5 руб/мин)"

def get_tariff_strategy(tariff_name: str) -> TariffStrategy:
    tariffs = {
        'Мобильный': MobileTariff(),
        'Домашний': HomeTariff(),
        'Премиум': PremiumTariff(),
    }
    return tariffs.get(tariff_name, MobileTariff())