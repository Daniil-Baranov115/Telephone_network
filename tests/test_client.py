import pytest
from app.models.Client import Client


def test_client_initial_balance():
    """Тест: Клиент создается с правильным балансом"""
    client = Client(id=1, name="Иван", balance=100.0, tariff_id=1)
    # Упадет, т.к. get_balance() не реализован
    assert client.get_balance() == 100.0


def test_client_add_balance():
    """Тест: Пополнение баланса"""
    client = Client(id=1, name="Иван", balance=100.0, tariff_id=1)
    client.add_balance(50.0)
    # Упадет
    assert client.get_balance() == 150.0


def test_client_deduct_balance_success():
    """Тест: Успешное списание"""
    client = Client(id=1, name="Иван", balance=100.0, tariff_id=1)
    result = client.deduct_balance(30.0)
    assert result == True
    assert client.get_balance() == 70.0


def test_client_deduct_balance_insufficient():
    """Тест: Ошибка при недостатке средств"""
    client = Client(id=1, name="Иван", balance=100.0, tariff_id=1)
    result = client.deduct_balance(150.0)
    assert result == False
    assert client.get_balance() == 100.0  # баланс не изменился