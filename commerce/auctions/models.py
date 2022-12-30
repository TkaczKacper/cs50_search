from django.contrib.auth.models import AbstractUser
from django.db import models
import decimal

class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="name")
    auction_image = models.URLField(default='https://t3.ftcdn.net/jpg/04/34/72/82/360_F_434728286_OWQQvAFoXZLdGHlObozsolNeuSxhpr84.jpg')
    category = models.CharField(max_length=64, default=None)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, default=decimal.Decimal(0))
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal(0))
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)


class AuctionBid(models.Model):
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="ID", default=None)
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, unique=True)
    bid_datetime = models.DateTimeField(default=None)
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_owner", default=None)

    def __str__(self):
        return f"{self.bid_owner}"

class AuctionComments(models.Model):
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="AuctionID", default=None)
    comment = models.CharField(max_length=255)
    comment_datetime = models.DateTimeField(default=None)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author", default=None)

class Watchlist(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist", default=None)
    auctionID = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_watchlist", default=None)

    def __str__(self):
        return f"{self.userID}, {self.auctionID}"
