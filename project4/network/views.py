import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Comments


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "number": paginator.num_pages,
        "site": "index"
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
    posts = Post.objects.filter(owner=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profil.html", {
        "user_data": user,
        "followers": followers,
        "posts": page_obj,
        "number": paginator.num_pages,
        "site": "profil"
    })


def following(request):
    try:
        followers = User.objects.get(username=request.user)
        posts = Post.objects.filter(owner__in=followers.followers.all()).order_by('-timestamp')
        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj,
            "number": paginator.num_pages,
            "site": "following"
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


def delete(request, post_id):
    try:
        site = request.POST["site_name"]
        post = Post.objects.get(id=post_id)
        if request.method == "POST":
            if post.owner == request.user:
                post.delete()
        if site == "profil":
            return HttpResponseRedirect(reverse(site, kwargs={'username':request.user.username}))
        else:
            return HttpResponseRedirect(reverse(site))
    except:
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == 'UPDATE':
        data = json.loads(request.body)
        if post.owner == request.user:
            if data.get("content") is not None:
                post.content = data["content"]
                post.save()
        return HttpResponse(status=204)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    if request.user not in User.objects.all():
        return JsonResponse({"error": "Log in to react."}, status=404)
    else:
        if request.method == "LIKE":
            post.likes.add(request.user)
            post.save()
            return JsonResponse({"success": "Liked"}, status=204)
        if request.method == "UNLIKE":
            post.likes.remove(request.user)
            post.save()
            return JsonResponse({"success": "Liked"}, status=204)
        else: 
            return HttpResponse(status=400)


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
