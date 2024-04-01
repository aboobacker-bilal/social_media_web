from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Bio = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField()

    def __str__(self):
        if self.name:
            return self.name
        return self.user.username


class Follow(models.Model):
    followers = models.ForeignKey(User, related_name="followers",
                                  on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following",
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.following} by {self.followers}"