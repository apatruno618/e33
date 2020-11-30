from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),

    # API
    path("customer", views.customer, name="customer"),
    path("category", views.category, name="category"),
    path("flavor", views.flavor, name="flavor"),
    path("product/<int:category_id>", views.product, name="product"),

]
