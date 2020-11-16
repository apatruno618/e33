import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):

    return render(request, "network/index.html")


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


@csrf_exempt
@login_required
def compose(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get content of post
    data = json.loads(request.body)
    user = request.user
    body = data.get("body", "")

    # Add new post to db
    post = Post(
        user=user,
        body=body
    )
    post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)


def posts(request):

    # Get posts from db
    posts = Post.objects.all()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


# @login_required
def profile_posts(request, user):

    # Get the user object to access id
    userObject = User.objects.filter(username=user)

    # Get that user's posts
    posts = Post.objects.filter(user=userObject[0].id)
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


def peopleWhoFollowThisUser(request, user):

    # Get the user object to access id
    userObject = User.objects.get(username=user)

    # Get number of followers
    followers = userObject.follower.count()

    return JsonResponse(followers, safe=False)


def peopleThisUserIsFollowing(request, user):

    # Get the user object to access id
    userObject = User.objects.get(username=user)
    # print(userObject)

    # Get all the account this user is following
    peopleFollowing = User.objects.filter(follower=userObject.id)
    print(peopleFollowing)
    following = 0
    for followingUser in peopleFollowing:
        if (user != followingUser.username):
            following += 1

    # Count the accounts
    # following = peopleFollowing.count()

    return JsonResponse(following, safe=False)
