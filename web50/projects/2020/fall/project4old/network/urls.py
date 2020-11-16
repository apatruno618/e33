
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.compose, name="compose"),
    path("posts/all", views.posts, name="posts"),
    path("posts/<str:user>", views.profile_posts, name="profile"),
    path("followers/<str:user>", views.peopleWhoFollowThisUser, name="followers"),
    path("following/<str:user>", views.peopleThisUserIsFollowing, name="following"),
]
