class BillingService:
    def __init__(self, client_repo, device_repo, call_repo):
        self.client_repo = client_repo
        self.device_repo = device_repo
        self.call_repo = call_repo
        self._strategy = None

    def set_tariff_strategy(self, strategy):
        """Устанавливает тарифный план"""
        self._strategy = strategy

    def process_call(self, from_device_id: int, duration_minutes: int) -> bool:
        """
        Обрабатывает звонок:
        - Находит клиента по устройству
        - Рассчитывает стоимость по тарифу
        - Проверяет баланс
        - Списывает деньги
        - Сохраняет звонок
        Возвращает True если успешно
        """
        pass

    def get_client_balance(self, client_id: int) -> float:
        """Возвращает баланс клиента"""
        pass