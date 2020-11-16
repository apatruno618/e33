from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField('self', blank=True)


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }


# class Followers(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE)
#     follower = models.ForeignKey("User", on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.follower is fo
