from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

# from .models import Bid, Comment, Listing, User
from .models import Comment, Listing, User


class ListingForm(ModelForm):
    # category = forms.CharField(initial="none")

    class Meta:
        model = Listing
        # fields = ['title', 'description', 'starting_bid', 'photo_link']
        # fields = '__all__'
        exclude = ['user', 'is_active', 'date_created']


def index(request):
    # displays active listings only
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
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
        # if request.POST.get('title') and request.POST.get('description') and request.POST.get('starting_bid'):

        #     title = request.POST["title"]
        #     description = request.POST["description"]
        #     starting_bid = int(request.POST["starting_bid"])
        #     photo_link = request.POST["photo_link"]
        #     # category = request.POST["category"]
        #     listing = Listing.save(
        #         title, description, starting_bid, photo_link)

        #     return HttpResponseRedirect(reverse("index"))
        form = ListingForm(request.POST)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        print(request.user)
        return render(request, "auctions/create.html", {
            'form': ListingForm()
        })


def listing(request, listing_id):
    # find the listing by its id
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "watchers": listing.watchers.all()
    })


def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment()
        comment.user = request.user
        comment.listing = listing
        comment.text = request.POST["text"]
        comment.save()
        # Comment.save(user=user, listing=listing_id,
        #              text=request.POST["text"])
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watch_add(request, listing_id):
    # print(listing_id)
    if request.method == "POST":
        # print(listing_id)
        listing = Listing.objects.get(pk=listing_id)
        watcher = request.user
        listing.watchers.add(watcher)

        # return render(request, "auctions/index.html", {
        #     "listings": Listing.objects.filter(is_active=True)
        # })
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watchlist(request):
    watcher = request.user
    listings = watcher.listings.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })
