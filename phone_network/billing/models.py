from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=50)
    price_per_minute = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)

    def get_balance(self):
        return float(self.balance)

    def add_balance(self, amount):
        self.balance += amount
        self.save()

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Device(models.Model):
    DEVICE_TYPES = [('mobile', 'Mobile'), ('home', 'Home')]
    phone_number = models.CharField(max_length=20, unique=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def get_number(self):
        return self.phone_number


class Call(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    duration_sec = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    from_device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='outgoing')
    to_device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='incoming')
