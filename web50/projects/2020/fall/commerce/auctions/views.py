from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import Bid, Category, Comment, Listing, User


class ListingForm(ModelForm):
    # form for creating a new listing
    class Meta:
        model = Listing
        exclude = ['user', 'is_active', 'date_created', 'watchers']


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
        # get form contents
        form = ListingForm(request.POST)
        if form.is_valid:
            # soft safe
            listing = form.save(commit=False)
            listing.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html", {
            'form': ListingForm()
        })


def listing(request, listing_id):
    # find the listing by its id
    listing = Listing.objects.get(pk=listing_id)
    # get comments related to the listing
    comments = Comment.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        # creates and saves new comment
        comment = Comment()
        comment.user = request.user
        comment.listing = listing
        comment.text = request.POST["text"]
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        watcher = request.user
        # removes listing from watchlist if it exists
        try:
            is_watching = watcher.listings.get()
            listing.watchers.remove(watcher)
        # otherwise adds it to watchlist
        except:
            listing.watchers.add(watcher)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def watchlist(request):
    watcher = request.user
    listings = watcher.listings.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def bid(request, listing_id):
    if request.method == "POST":
        bidder = request.user
        bid = float(request.POST["bid"])
        listing = Listing.objects.get(pk=listing_id)
        try:
            # gets the highest current bid
            highest_bid = Bid.objects.filter(
                listing=listing_id).order_by('-bid')[0]
            # save the new bid if its higher than the highest bid
            if bid > highest_bid.bid:
                new_bid = Bid()
                new_bid.user = bidder
                new_bid.listing = listing
                new_bid.bid = bid
                new_bid.save()
                messages.success(request, "Your bid was accepted!")
        # there's no bid in the bid table
        except IndexError:
            # save the new bid if its higher than the starting bid
            if bid > listing.starting_bid:
                new_bid = Bid()
                new_bid.user = bidder
                new_bid.listing = listing
                new_bid.bid = bid
                new_bid.save()
                messages.success(request, "Your bid was accepted!")
            else:
                messages.error(
                    request, "Your bid was too low. Please place a higher bid.")
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    print(category_id)
    # return render(request, "auctions/categories.html", {
    #     "categories": Category.objects.all()
    # })
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category_id)
    })
