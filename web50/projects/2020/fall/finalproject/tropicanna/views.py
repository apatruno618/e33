import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Customer, Category, Flavor, Product


def index(request):
    return render(request, "tropicanna/index.html", {
        "all_categories": Category.objects.all(),
        "all_flavors": Flavor.objects.all(),
        "customers": Customer.objects.all()
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


@login_required
def order(request):

    # Submitting an order
    if request.method == "POST":
        # data = json.loads(request.body)
        data = request.body
        print(data)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "tropicanna/order.html", {
            "customers": Customer.objects.all(),
            "all_categories": Category.objects.all(),
        })


@csrf_exempt
@login_required
def customer(request):

    # Saving a new customer must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the new customer info
    data = json.loads(request.body)
    name = data["customerName"]
    phone = int(data["customerPhone"])

    if name == [""]:
        return JsonResponse({"error": "Must include a name."}, status=400)

    # Save new customer to db
    customer = Customer(name=name, phone=phone)
    customer.save()

    return JsonResponse({"message": "Customer saved successfully."}, status=201)


@csrf_exempt
@login_required
def category(request):

    # Saving a new category must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the new category info
    data = json.loads(request.body)
    name = data["categoryName"]
    price = float(data["categoryPrice"])
    # print(type(price))

    if name == [""] or price == [""]:
        return JsonResponse({"error": "A new category must have a name and price."}, status=400)

    category = Category(name=name, price=price)
    category.save()

    return JsonResponse({"message": "Category saved successfully."}, status=201)


@csrf_exempt
@login_required
def flavor(request):

    # Saving a new flavor must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

        # Get the new category info
    data = json.loads(request.body)
    name = data["flavorName"]

    if name == [""]:
        return JsonResponse({"error": "A new flavor must have a name."}, status=400)

    flavor = Flavor(name=name)
    flavor.save()

    return JsonResponse({"message": "Flavor saved successfully."}, status=201)


@csrf_exempt
@login_required
def product(request, category_id):

    # Saving a new flavor must be via POST
    # if request.method != "POST":
    # return JsonResponse({"error": "POST request required."}, status=400)

    category = Category.objects.get(pk=category_id)
    flavors = category.flavors.all()
    non_flavors = Flavor.objects.exclude(categories=category).all()
    # print(non_flavors)
    # Finding the flavor id and category from the submitted form data
    # flavor_id = int(request.POST["flavor"])
    # category_id = int(request.POST["category"])

    # Finding the category based on the id
    # category = Category.objects.get(pk=category_id)

    # Add flavor to the category
    # category.flavors.add(flavor)

    # return JsonResponse({"message": "Flavor saved successfully."}, status=201)

    return render(request, "tropicanna/product.html", {
        "category": category,
        "flavors": flavors,
        "non_flavors": non_flavors
    })


@login_required
def add_flavor(request, category_id):

    # For a post request, add a new flavor
    if request.method == "POST":

        # Accessing the product
        category = Category.objects.get(pk=category_id)

        # Finding the passenger id from the submitted form data
        flavor_id = int(request.POST["flavor"])

        # Finding the passenger based on the id
        flavor = Flavor.objects.get(pk=flavor_id)

        # Add passenger to the flight
        category.flavors.add(flavor)

        # Redirect user to flight page
        return HttpResponseRedirect(reverse("product", args=(category.id,)))
