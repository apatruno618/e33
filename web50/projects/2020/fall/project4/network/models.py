from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.decorators import login_required


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }


class Follower(models.Model):
    subject = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE)

    def serialize(self):
        return {
            "subject": self.subject,
            "follow": self.follower
        }
