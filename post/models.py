from django.db import models
from django.contrib.auth.models import User
from user.models import UserProfile

# Create your models here.


class Post(models.Model):
    image = models.ImageField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}, {self.caption}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"

