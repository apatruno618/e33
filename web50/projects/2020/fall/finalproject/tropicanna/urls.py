from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),
    path("product/<int:category_id>", views.product, name="product"),
    path("<int:category_id>/add_flavor", views.add_flavor, name="add_flavor"),

    # API
    path("customer", views.customer, name="customer"),
    path("category", views.category, name="category"),
    path("flavor", views.flavor, name="flavor"),


]
