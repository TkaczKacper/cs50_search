from django.contrib import admin

from .models import Auction, AuctionBid, AuctionComments, User, Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(AuctionBid)
admin.site.register(AuctionComments)
admin.site.register(Watchlist)