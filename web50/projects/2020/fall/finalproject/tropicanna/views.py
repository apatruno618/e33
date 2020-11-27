from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User, Customer, Category, Flavor, Product

# Create your views here.


def index(request):

    category = Category.objects.get(name="1/2 Gal. Tropics")
    # print(category)
    products_by_category = category.products.all()
    # print(products_by_category)
    flavor = Flavor.objects.get(name="Pineapple")
    print(flavor)
    products_by_flavor = flavor.products.all()
    print(products_by_flavor)

    return render(request, "tropicanna/index.html", {
        "customers": Customer.objects.all(),
        "products": products_by_category,
        "categories": Category.objects.all(),
        "flavors": products_by_flavor
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
            return render(request, "tropicanna/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tropicanna/login.html")


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
            return render(request, "tropicanna/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tropicanna/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tropicanna/register.html")
