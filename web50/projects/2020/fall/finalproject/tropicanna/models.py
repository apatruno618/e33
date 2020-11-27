from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }


class Category(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }


class Flavor(models.Model):
    name = models.CharField(max_length=100)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Product(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products")
    flavor = models.ForeignKey(
        "Flavor", on_delete=models.CASCADE, related_name="products")

    def serialize(self):
        return {
            "id": self.id,
            "category": self.category,
            "flavor": self.flavor
        }
