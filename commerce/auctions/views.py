from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django import forms
from datetime import datetime, timedelta
from decimal import Decimal

from .models import User, Auction, AuctionBid, AuctionComments, Watchlist
from .forms import CreateListingForm, MakeBid, AddComment


def index(request):
    auctions = Auction.objects.filter(end_date__gte = timezone.now())
    return render(request, "auctions/index.html", {
        'Auctions': auctions,
    })

def categories(request):
    categories = ['Sport', 'Jewelry', 'Decorations', 'Books', 'Automotive', 'Electronics', 'Toys']
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, name):
    auctions = Auction.objects.filter(end_date__gte = timezone.now(), category=name)
    print(auctions)
    return render(request, "auctions/category.html", {
        "auctions": auctions
    })


@login_required
def watchlist(request):
    watchlist_entries = Watchlist.objects.filter(userID=request.user)

    watchlist_auctions = []
    for i in watchlist_entries:
        watchlist_auctions.append(Auction.objects.get(end_date__gte = timezone.now(), pk=i.auctionID.pk))

    return render(request, "auctions/watchlist.html", {
        'Watchlist': watchlist_auctions
    })


@login_required
def listing(request, number):
    auction = Auction.objects.get(pk=number)
    bids = AuctionBid.objects.filter(auctionID = auction)
    current_winner = bids.last()
    comments = AuctionComments.objects.filter(auctionID = auction)
    initial_bid = auction.current_bid + Decimal(0.01)
    if initial_bid < 0.011:
        initial_bid = auction.starting_bid
    initial_data = {
        'bid': '{0:.2f}'.format(initial_bid)
    }
    bid_form = MakeBid(initial=initial_data)
    comment_form = AddComment()

    on_watchlist = False
    try:
        if Watchlist.objects.get(userID=request.user, auctionID=auction):
            on_watchlist = True
    except:
        pass
        

    active = True
    if auction.end_date < timezone.now():
        active = False
    return render(request, "auctions/listings.html", {
        "active": active,
        "on_watchlist": on_watchlist,
        "auction": auction,
        "bid_form": bid_form,
        "bids": bids,
        "comment_form": comment_form,
        "comments": comments,
        "winner": current_winner,
    })

@login_required
def add_comment(request, number):
    comment = AuctionComments()
    comment.comment = request.POST.get('comment')
    comment.comment_author = request.user
    comment.comment_datetime = datetime.now() 
    comment.auctionID = Auction.objects.get(pk=number)
    comment.save()
    return redirect(reverse('listings', kwargs={'number':number}))

@login_required
def make_bid(request, number):
    posted_bid = request.POST.get('bid')
    auctionID = Auction.objects.get(pk=number)
    try:
        if AuctionBid.objects.filter(auctionID=number).order_by('-bid').first().bid_owner == request.user:
            messages.error(request, "You can't outbid yourself.")
            return redirect(reverse('listings', kwargs={'number':number}))
        highest_bid = AuctionBid.objects.filter(auctionID=number).order_by('-bid').first().bid
        if Decimal(posted_bid) <= highest_bid:
            messages.error(request, "You can't offer less than curret winner.")
            return redirect(reverse('listings', kwargs={'number':number}))
    except:
        pass
    if Decimal(posted_bid) < auctionID.starting_bid:
        messages.error(request, "You can't offer less than starting price.")
        return redirect(reverse('listings', kwargs={'number':number}))
    
    bid = AuctionBid()
    Auction.objects.filter(pk=number).update(current_bid=posted_bid)
    bid.bid = posted_bid
    bid.auctionID = Auction.objects.get(pk=number)
    bid.bid_datetime = datetime.now()
    bid.bid_owner = request.user
    bid.save()
    return redirect(reverse('listings', kwargs={'number':number}))

@login_required
def finish_auction(request, number):
    Auction.objects.filter(pk=number).update(end_date=timezone.now())
    return redirect(reverse('listings', kwargs={'number':number}))

@login_required
def add_to_watchlist(request, number):
    watchlist = Watchlist()
    watchlist.auctionID = Auction.objects.get(pk=number)
    watchlist.userID = request.user
    watchlist.save()
    return redirect(reverse('listings', kwargs={'number':number}))

@login_required
def remove_from_watchlist(request, number):
    Watchlist.objects.filter(auctionID=Auction.objects.get(pk=number), userID=request.user).delete()
    return redirect(reverse('listings', kwargs={'number':number}))

@login_required
def create_listing(request):
    form = CreateListingForm()
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = Auction()
            listing.title = form.cleaned_data.get('title')
            listing.description = form.cleaned_data.get('description')
            listing.owner = request.user
            if form.cleaned_data.get('auction_image'):
                listing.auction_image = form.cleaned_data.get('auction_image')
                print(listing.auction_image)
            listing.starting_bid = form.cleaned_data.get('starting_bid')
            listing.start_date = datetime.now()
            listing.end_date = listing.start_date + timedelta(hours= form.cleaned_data.get('duration'))
            listing.category = form.cleaned_data.get('category')
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {
        'form': form
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
