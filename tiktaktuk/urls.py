from django.shortcuts import redirect
from django.urls import path, include

from accounts.views import home


urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", lambda request: redirect("accounts:dashboard")),
    path("login/", lambda request: redirect("accounts:login")),
    path("register/", lambda request: redirect("accounts:register")),
    path("accounts/", include("accounts.urls")),
    path("artists/", include("artists.urls")),
    path("orders/", include("orders.urls")),
]
