
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makepost", views.makepost, name = "makepost"),
    path("loadpage/<str:dir>", views.directory, name = "directory"),
    path("loadpage/profile/<int:id>", views.profile, name = "profile"),
    path("like", views.leavealike, name = "leavealike")
]
