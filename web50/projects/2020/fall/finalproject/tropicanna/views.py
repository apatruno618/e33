from django.shortcuts import render

from .models import Customer

# Create your views here.


def index(request):
    return render(request, "index.html", {
        "customers": Customer.objects.all()
    })
