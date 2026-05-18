from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=50)
    price_per_minute = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.name} ({self.price_per_minute} руб/мин)"

    class Meta:
        db_table = 'tariffs'


class Client(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField(default=0.0)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50, unique=True, default='user')
    password = models.CharField(max_length=128, default='password')
    is_admin = models.BooleanField(default=False)

    def get_balance(self) -> float:
        return self.balance

    def add_balance(self, amount: float) -> None:
        self.balance += amount
        self.save(update_fields=['balance'])

    def deduct_balance(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.save(update_fields=['balance'])
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'clients'


class Device(models.Model):
    DEVICE_TYPES = [
        ('mobile', 'Мобильный'),
        ('home', 'Домашний'),
    ]
    phone_number = models.CharField(max_length=20, unique=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='devices')

    def get_number(self) -> str:
        return self.phone_number

    def __str__(self):
        return f"{self.get_number()} ({self.get_device_type_display()})"

    class Meta:
        db_table = 'devices'


class Call(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    duration_sec = models.IntegerField()
    cost = models.FloatField(default=0.0)
    from_device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='outgoing_calls')
    to_device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='incoming_calls')

    def __str__(self):
        return f"Call from {self.from_device.phone_number} to {self.to_device.phone_number}"

    class Meta:
        db_table = 'calls'
