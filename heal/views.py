from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    return render(request, "heal/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("heal:index"))
        else:
            return render(request, "heal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "heal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("heal:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "heal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "heal/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("heal:index"))
    else:
        return render(request, "heal/register.html")

def community(request):
    if request.user is None:
        return HttpResponseRedirect(reverse("heal:login"))
    post_list = UserPost.objects.all().order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "heal/community.html", {
        "posts": posts,
        "curruser": request.user,
    })

@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        post = UserPost.objects.get(id=post_id)
        post.content = new_post
        post.save()
        try:
            post = UserPost.objects.get(id=post_id)
            if post.user == request.user:
                post.post = new_post.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)

def makepost(request):
    if request.user is None:
        return HttpResponseRedirect(reverse("heal:login"))
    if request.method =="POST":
        postreq = request.POST["content"]
        p = UserPost(user=request.user, content=postreq)
        p.save()
    return HttpResponseRedirect(reverse("heal:community"))

def profile(request, userid):
    if request.user is None:
        return HttpResponseRedirect(reverse("heal:login"))
    user = User.objects.all().filter(pk=userid)[0]
    return render(request, "heal/profile.html", {
        "user": request.user,
        "profuser": user,
        "posts": UserPost.objects.all().filter(user=user).order_by('-timestamp')
    })
