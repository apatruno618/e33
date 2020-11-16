import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.forms import ModelForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follower


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'timestamp']


def index(request):
    # Get posts from db and return in reverse chronological order
    posts = Post.objects.order_by("-timestamp").all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)

    paginated_posts = paginator.page(page)

    return render(request, "network/index.html", {"title": "All Posts", "posts": paginated_posts})


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


@login_required
def create(request):
    if request.method == "POST":
        # get form contents
        form = CreatePostForm(request.POST)
        if form.is_valid:
            # soft save
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/create.html", {
            'form': CreatePostForm()
        })


def profile(request, user_id):
    # Find users posts
    posts = Post.objects.filter(author=user_id).order_by("-timestamp").all()
    user_profile = User.objects.get(id=user_id)
    followers = user_profile.followers.count()
    user_is_following = Follower.objects.filter(follower=user_profile).count()

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)

    paginated_posts = paginator.page(page)

    on_followerlist = False
    for follower in user_profile.followers.all():
        if follower.follower == request.user:
            on_followerlist = True

    return render(request, "network/profile.html", {"user_profile": user_profile, "posts": paginated_posts, "followers": followers, "user_is_following": user_is_following, "on_followlist": on_followerlist})


def unfollow(request):
    # This does not work but my logic is in the comments
    if request.method == "POST":
        # Get the follower
        follower = get_object_or_404(User, username=follower)
        # Get the subject we're interested in
        subject = get_object_or_404(
            Follower, subject=int(request.POST["user_id"]))
        # Remove the follower from the subject's follower list
        subject.followers.remove(follower)
        # Send the user back to the subject's profile
        return HttpResponseRedirect(reverse("profile", args=(int(request.POST["user_id"],))))


def follow(request):
    # This does not work but my logic is in the comments
    if request.method == "POST":
        # Get the follower
        follower = get_object_or_404(User, username=follower)
        # Get the subject we're interested in
        subject = get_object_or_404(
            Follower, subject=int(request.POST["user_id"]))
        # Add the follower to the subject follower list
        subject.followers.add(follower)
        # Send the user back to the subject's profile
        return HttpResponseRedirect(reverse("profile", args=(int(request.POST["user_id"],))))


@login_required
def followlist(request):
    # This does not work but my logic is in the comments
    #  Get accounts the request.user is following
    followlist = Follower.objects.filter(follower=request.user)
    # Get posts from each of the accounts request.user is following
    myposts = Post.objects.filter(author=request.user)

    # Ideally the only line needed would be
    posts = request.user.followers.posts.order_by("-creation_time").all()

    return render(request, "network/index.html", {
        "title": "Following",
        "posts": posts
    })


@csrf_exempt
@login_required
def edit(request, post_id):

    # Query for post
    try:
        post = Post.objects.get(author=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
            print(data["body"])
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def like(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        post.likes += 1
        post.save()
        return HttpResponse(status=204)
