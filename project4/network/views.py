from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Post, Comments


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts
    })


def add_post(request):
    if request.method == "POST":
        post = Post()
        post.content = request.POST["post_content"]
        post.owner = request.user
        post.timestamp = timezone.now()
        post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


def profil(request, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        message = "stop playing with links"
        return render(request, "network/profil.html", {
            "message": message
        })
    followers = user.followers.all()
    posts = Post.objects.filter(owner=user)
    return render(request, "network/profil.html", {
        "user_data": user,
        "followers": followers,
        "posts": posts
    })


def following(request):
    try:
        followers = User.objects.get(username=request.user)
        posts = Post.objects.filter(owner__in=followers.followers.all())
        return render(request, "network/index.html", {
            "posts": posts
        })
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('login'))


def follow(request, username):
    if request.method == "POST":
        user_profil = User.objects.get(username=username)
        if request.user in user_profil.followers.all():
            user_profil.followers.remove(User.objects.get(username=request.user))
            user_profil.save()
        else:
            user_profil.followers.add(User.objects.get(username=request.user))
            user_profil.save()
    return HttpResponseRedirect(reverse('profil',  kwargs={'username':username}))


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
