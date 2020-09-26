from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:entry>", views.content, name="content")
]
