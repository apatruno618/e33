from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    photo_link = models.URLField()
    category = models.CharField(max_length=64)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()

    def __str__(self):
        return f"{self.title} listed for: {self.starting_bid}"


class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField()

    def __str__(self):
        return f"bid of {self.bid} on {self.listing_id}"


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date_created = models.DateTimeField()

    def __str__(self):
        return f"{self.user_id} commented {self.comment}"
