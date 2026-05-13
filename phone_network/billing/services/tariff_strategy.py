from abc import ABC, abstractmethod


class TariffStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, duration_minutes: int) -> float:
        pass


class MobileTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 1.0

    def get_name(self):
        return "Мобильный (1 руб/мин)"


class HomeTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 0.5

    def get_name(self):
        return "Домашний (0.5 руб/мин)"


class PremiumTariff(TariffStrategy):
    def calculate_cost(self, duration_minutes: int) -> float:
        return duration_minutes * 1.5

    def get_name(self):
        return "Премиум (1.5 руб/мин)"
