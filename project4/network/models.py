from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner", default=None)
    timestamp = models.DateTimeField(default=None)
    content = models.CharField(max_length=2500, default=None)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likers", default=None)

class Comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_id", default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner", default=None)
    timestap = models.DateTimeField(default=None)
    likes = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likers", default=None)
    content = models.CharField(max_length=1000, default=None)

class Relations(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_follower", default=None)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relation_following", default=None)