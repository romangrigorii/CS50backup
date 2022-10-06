import json
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

@csrf_exempt
@login_required
def leavealike(request):
    if request.method != "POST":
        return JsonResponse({"error" : "PUT request required to leave a like"}, status = 400)
    data = json.loads(request.body)
    postid = data.get("postid")
    post = Post.objects.get(id = int(postid))
    account = Account.objects.get(owner = request.user)
    if len(post.likes.filter(id = account.id)) == 0:
            post.likes.add(account)
    else:
        post.likes.remove(post.likes.get(id = account.id))
    # if post.poster.id != account.id:
    #     if len(post.likes.filter(id = account.id)) == 0:
    #         post.likes.add(account)
    #     else:
    #         post.likes.remove(post.likes.get(id = account.id))
    # else:
    #     return JsonResponse({"error" : "Can't like your own stuff you narcisist! "}, status = 400)
    # post.likes.add(account)
    return JsonResponse({"message" : "left a like! "}, status = 201)


def index(request):
    # when we navigate to index we check if the owner of the account is registered as such
    # and tie them to an account if not
    if len(Account.objects.filter(owner = request.user.id)) == 0:
        account = Account(owner = request.user)
        account.save()
    posts = Post.objects.all()
    return render(request, "network/index.html",{
        "posts": posts,
    })

@csrf_exempt
@login_required
def makepost(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    message = data.get("message", "")
    if message == "":
        return JsonResponse({"error": "Your posts cannot have empty messages. You can use twitter for that. "}, status=400)
    post = Post(poster = Account.objects.get(owner = request.user), message = message)
    post.save()
    return JsonResponse({"message": "Posted sucessfully."}, status=201)


def directory(request, dir):
    account = Account.objects.get(owner = request.user)
    if dir == "profile":
        posts = Post.objects.filter(poster = account)
    elif dir == "mainpage":
        posts = Post.objects.all()
    elif dir == "following":
        for account in account.following.all():
            posts.append(Post.objects.filter(poster = account))
    else:
        return JsonResponse({"error": "Nonexistant directory."}, status=400)
    if len(posts)>0:
        posts = posts.order_by("-timestamp").all()

    return JsonResponse([account.serialize(),[post.serialize() for post in posts]], safe = False) # this will simply be the response to fetch 

def profile(request, id):
    # return JsonResponse([{"accid" : Account.objects.get(owner = request.user).id},[post.serialize() for post in Post.objects.filter(poster = Account.objects.get(owner = request.user))]])
    return JsonResponse({"accid" : id == Account.objects.get(owner = request.user).id})


def postaccess(request, postid):
    if len(Post.objects.filter(id = postid)) == 0:
        return JsonResponse({"error": "No such post."}, status=400)
    else:
        post = Post.objects.filter(id = postid);
        return JsonResponse(post.serialize())

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
