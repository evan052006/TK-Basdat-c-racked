import jwt

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from orders.queries import orders_db
from artists.queries import artists_db
from .decorators import require_roles
from .queries import accounts_db


ROLE_RANK = {"GUEST": 0, "CUSTOMER": 1, "ORGANIZER": 2, "ADMIN": 3}


def _role_names(user_id):
    return [role["role_name"] for role in accounts_db.get_user_roles(user_id=user_id)]


def _issue_login_response(user, role_name):
    refresh = RefreshToken()
    refresh["user_id"] = str(user["user_id"])
    refresh["active_role"] = role_name

    response = redirect("accounts:dashboard")
    response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        httponly=True,
        samesite="Lax",
        secure=False,
    )
    return response


def _current_user(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return accounts_db.get_acc_by_id(user_id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
        return None


def _safe_count(callback, fallback=0):
    try:
        return callback()
    except Exception:
        return fallback


def home(request):
    if request.COOKIES.get("access_token"):
        return redirect("accounts:dashboard")
    return redirect("accounts:login")


@require_roles("CUSTOMER", "ORGANIZER", "ADMIN")
def dashboard(request):
    user = _current_user(request) or {}
    role = request.user_role if hasattr(request, "user_role") else "GUEST"

    orders = list(_safe_count(orders_db.get_orders, []))
    promotions = list(_safe_count(orders_db.get_promotions, []))

    context = {
        "dashboard_user": user,
        "role": role,
        "artist_count": _safe_count(artists_db.get_artist_count),
        "genre_count": _safe_count(artists_db.get_genre_count),
        "order_count": len(orders),
        "promotion_count": len(promotions),
        "revenue_total": sum(float(order.get("total_amount") or 0) for order in orders),
        "active_promotions": len(promotions),
    }
    return render(request, "dashboard.html", context)


def register(request):
    if request.method == "GET":
        roles = accounts_db.get_roles()
        return render(request, "register.html", {"roles": roles})

    if request.method == "POST":
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        roles = accounts_db.get_roles()
        selected_role_id = request.POST.get("role")

        if not selected_role_id:
            legacy_role_ids = request.POST.getlist("roles")
            selected_role_id = legacy_role_ids[0] if len(legacy_role_ids) == 1 else None

        if not selected_role_id:
            return render(
                request,
                "register.html",
                {"roles": roles, "error": "Pilih satu jenis pengguna."},
            )

        selected_role = accounts_db.get_role_by_id(role_id=selected_role_id)
        if selected_role is None:
            return render(
                request,
                "register.html",
                {"roles": roles, "error": "Role tidak valid."},
            )

        hashed_password = make_password(raw_password)
        existing_user = accounts_db.get_acc_by_username(username=username)

        with accounts_db.transaction():
            if existing_user is not None:
                if not check_password(raw_password, existing_user["password"]):
                    return render(
                        request,
                        "register.html",
                        {
                            "roles": roles,
                            "error": "Username sudah terdaftar. Masukkan password yang sama untuk menambah role baru.",
                        },
                    )

                existing_roles = _role_names(existing_user["user_id"])
                if selected_role["role_name"] in existing_roles:
                    return render(
                        request,
                        "register.html",
                        {
                            "roles": roles,
                            "error": "Akun ini sudah memiliki role tersebut.",
                        },
                    )

                accounts_db.insert_roles(
                    user_id=existing_user["user_id"], role_id=selected_role_id
                )
                return redirect("accounts:login")

            user_id = accounts_db.create_user(
                username=username, password=hashed_password
            )
            accounts_db.insert_roles(user_id=user_id, role_id=selected_role_id)

        return redirect("accounts:login")


def select_role(request):
    pending_user_id = request.session.get("pending_user_id")
    if not pending_user_id:
        return redirect("accounts:login")

    user = accounts_db.get_acc_by_id(user_id=pending_user_id)
    if user is None:
        request.session.pop("pending_user_id", None)
        return redirect("accounts:login")

    roles = accounts_db.get_user_roles(user_id=pending_user_id)

    if request.method == "GET":
        return render(request, "select_role.html", {"roles": roles})

    selected_role = request.POST.get("role")
    role_names = [role["role_name"] for role in roles]
    if selected_role not in role_names:
        return render(
            request,
            "select_role.html",
            {"roles": roles, "error": "Pilih role login yang valid."},
        )

    request.session.pop("pending_user_id", None)
    return _issue_login_response(user, selected_role)


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = accounts_db.get_acc_by_username(username=username)

        if user is not None and check_password(password, user["password"]):
            roles = _role_names(user["user_id"])
            if len(roles) > 1:
                request.session["pending_user_id"] = str(user["user_id"])
                return redirect("accounts:select_role")

            if roles:
                return _issue_login_response(user, roles[0])

            return render(
                request,
                "login.html",
                {"error": "Akun belum memiliki role."},
            )

        return render(request, "login.html", {"error": "Invalid credentials"})


def logout(request):
    response = redirect("accounts:login")
    response.delete_cookie("access_token")
    request.session.flush()
    return response


@require_roles("CUSTOMER", "ORGANIZER", "ADMIN")
def profile(request):
    user = _current_user(request)
    if not user:
        return redirect("accounts:login")

    role = request.user_role if hasattr(request, "user_role") else "GUEST"
    user_id = str(user["user_id"])
    editing = request.GET.get("edit") == "1"
    success = None
    error = None

    # Load role-specific profile
    profile_data = None
    if role == "CUSTOMER":
        profile_data = accounts_db.get_customer_by_user_id(user_id=user_id)
    elif role == "ORGANIZER":
        profile_data = accounts_db.get_organizer_by_user_id(user_id=user_id)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            if role == "CUSTOMER":
                accounts_db.update_customer_profile(
                    full_name=request.POST.get("full_name"),
                    phone_number=request.POST.get("phone_number"),
                    user_id=user_id,
                )
                profile_data = accounts_db.get_customer_by_user_id(user_id=user_id)
            elif role == "ORGANIZER":
                accounts_db.update_organizer_profile(
                    organizer_name=request.POST.get("organizer_name"),
                    contact_email=request.POST.get("contact_email"),
                    user_id=user_id,
                )
                profile_data = accounts_db.get_organizer_by_user_id(user_id=user_id)
            success = "Profil berhasil diperbarui."
            editing = False

        elif form_type == "password":
            old_pw = request.POST.get("old_password")
            new_pw = request.POST.get("new_password")
            confirm_pw = request.POST.get("confirm_password")

            if not check_password(old_pw, user["password"]):
                error = "Password lama tidak sesuai."
            elif new_pw != confirm_pw:
                error = "Konfirmasi password baru tidak cocok."
            elif len(new_pw) < 6:
                error = "Password baru minimal 6 karakter."
            else:
                hashed = make_password(new_pw)
                accounts_db.update_user_password(user_id=user_id, password=hashed)
                success = "Password berhasil diperbarui."

    initial = (user.get("username") or "?")[0].upper()

    return render(request, "profile.html", {
        "dashboard_user": user,
        "user": user,
        "role": role,
        "profile": profile_data,
        "initial": initial,
        "editing": editing,
        "success": success,
        "error": error,
    })
