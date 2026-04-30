import jwt
from functools import wraps
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import UserAccount
from .queries import accounts_db


ROLE_RANK = {"GUEST": 0, "CUSTOMER": 1, "ORGANIZER": 2, "ADMIN": 3}


def require_roles(*allowed_roles):
    """
    Decorator for HTML views that checks for a valid JWT in cookies
    and verifies the user has at least one of the allowed roles.
    Usage: @require_roles('ADMIN', 'EDITOR')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            token = request.COOKIES.get("access_token")

            if not token:
                if "GUEST" in allowed_roles:
                    request.user_role = "GUEST"
                    return view_func(request, *args, **kwargs)
                return redirect("accounts:login")

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
                active_role = payload.get("active_role")
                user_roles = [
                    role["role_name"]
                    for role in accounts_db.get_user_roles(user_id=user_id)
                ]
                if active_role not in user_roles:
                    active_role = user_roles[0] if user_roles else "GUEST"
                request.user_role = active_role

                allowed_rank = min(ROLE_RANK.get(role, 99) for role in allowed_roles)
                is_authorized = ROLE_RANK.get(active_role, 0) >= allowed_rank

                if not is_authorized:
                    return HttpResponseForbidden(
                        "<h1>403 Forbidden</h1><p>You don't have the required role to view this page.</p>"
                    )

            except jwt.ExpiredSignatureError:
                return redirect("accounts:login")
            except (jwt.InvalidTokenError, UserAccount.DoesNotExist):
                return redirect("accounts:login")
            except Exception:
                return redirect("accounts:login")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
