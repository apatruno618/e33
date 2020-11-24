from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }
