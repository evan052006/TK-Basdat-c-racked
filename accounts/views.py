from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .queries import accounts_db
from .decorators import require_roles


def register(request):
    if request.method == "GET":
        roles = accounts_db.get_roles()
        return render(request, "register.html", {"roles": roles})

    if request.method == "POST":
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        selected_role_ids = request.POST.getlist("roles")

        hashed_password = make_password(raw_password)

        with accounts_db.transaction():
            if accounts_db.get_acc_by_username(username=username) is not None:
                return render(
                    request,
                    "register.html",
                    {"error": "Username already exists"},
                )
            user_id = accounts_db.create_user(
                username=username, password=hashed_password
            )
            for role in selected_role_ids:
                accounts_db.insert_roles(user_id=user_id, role_id=role)

        return redirect("accounts:login")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = accounts_db.get_acc_by_username(username=username)

        if user is not None and check_password(password, user["password"]):
            refresh = RefreshToken()
            refresh["user_id"] = str(user["user_id"])

            access_token = str(refresh.access_token)

            response = redirect("accounts:register")

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="Lax",
                secure=False,
            )

            return response

        return render(request, "login.html", {"error": "Invalid credentials"})


@require_roles("ADMIN")
def logout(request):
    response = redirect("accounts:login")
    response.delete_cookie("access_token")
    return response
