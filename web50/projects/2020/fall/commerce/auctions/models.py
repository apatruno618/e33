from django.contrib.auth.models import AbstractUser
from django.db import models

# blank=True, null=True


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=20, default="none")

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    # optional field
    photo_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(
        User, blank=True, related_name="listings")

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


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is watching {self.listing}"