from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Flavor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    flavors = models.ManyToManyField(
        Flavor, blank=True, related_name="categories")

    def __str__(self):
        return f"{self.name}, retails for {self.price}"


class Order(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="orders")
    delivered = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.customer} placed an order for ${self.order_total} on {self.order_date}"


class OrderedItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    flavor = models.ForeignKey("Flavor", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    category_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Prepare {self.quantity} case(s) of {self.category.name} {self.flavor} for {self.order.customer}"
