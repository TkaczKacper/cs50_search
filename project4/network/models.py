from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True, related_name="followers")
    following = models.ManyToManyField("self", blank=True, related_name="following")

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner", default=None)
    timestamp = models.DateTimeField(default=None)
    content = models.CharField(max_length=2500, default=None)
    likes = models.ManyToManyField(User, blank=True, related_name="likers")

class Comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_id", default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner", default=None)
    timestamp = models.DateTimeField(default=None)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likers")
    content = models.CharField(max_length=1000, default=None, null=True)
