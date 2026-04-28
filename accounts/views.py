from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAccount, Role
from .queries import accounts_db


def register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    if request.method == "POST":
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        selected_role_ids = request.POST.getlist("roles")

        if UserAccount.objects.filter(username=username).exists():
            roles = Role.objects.all()
            return render(
                request,
                "accounts/register.html",
                {"roles": roles, "error": "Username already exists"},
            )

        hashed_password = make_password(raw_password)

        with accounts_db.transaction():
            user_id = accounts_db.create_user(
                username=username, password=hashed_password
            )
            data_to_insert = [
                {"user_id": user_id, "role_id": role_id}
                for role_id in selected_role_ids
            ]
            accounts_db.insert_roles(data_to_insert)

        return redirect("login")


def login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = accounts_db.get_acc_by_username(username)

        if user is not None and check_password(password, user["password"]):
            refresh = RefreshToken.for_user(user["user_id"])
            access_token = str(refresh.access_token)

            response = redirect("home")

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="Lax",
                secure=False,
            )

            return response

        return render(request, "accounts/login.html", {"error": "Invalid credentials"})


def logout(request):
    response = redirect("login")
    response.delete_cookie("access_token")
    return response
