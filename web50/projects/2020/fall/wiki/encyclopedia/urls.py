from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("add", views.add, name="add"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("update", views.update, name="update"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.content, name="content")
]
