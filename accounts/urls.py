from django.urls import path
from .views import dashboard, login, register, select_role, logout, profile

app_name = "accounts"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", login, name="login"),
    path("select-role/", select_role, name="select_role"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
]
