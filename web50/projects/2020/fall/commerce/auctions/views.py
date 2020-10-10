from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from .models import Bid, Comment, Listing, User
from .models import Comment, Listing, User

# class NewTaskForm(forms.Form):
#     title = forms.CharField(label="Title")
#     description = forms.CharField(widget=forms.Textarea)
# 	starting_bid = forms.


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def create(request):
    if request.method == "POST":
        if request.POST.get('title') and request.POST.get('description') and request.POST.get('starting_bid'):

            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = int(request.POST["starting_bid"])
            photo_link = request.POST["photo_link"]
            # category = request.POST["category"]
            listing = Listing.save(
                title, description, starting_bid, photo_link)

            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")


def listing(request, listing_id):
    # find the listing by its id
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def comment(request):
    if request.method == "POST":
        new_comment = request.POST["comment"]
