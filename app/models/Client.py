class Client:

    def __init__(self, id: int, name: str, balance: float, tariff_id: int):
        self.id = id
        self.name = name
        self.balance = balance
        self.tariff_id = tariff_id

    def get_balance(self) -> float:
        pass

    def add_balance(self, amount: float) -> None:
        pass

    def deduct_balance(self, amount: float) -> bool:
        pass
