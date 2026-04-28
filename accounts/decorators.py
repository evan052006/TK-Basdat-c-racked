import jwt
from functools import wraps
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import UserAccount
from .queries import accounts_db


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
                return redirect("login_page")

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")

                is_authorized = accounts_db.has_any_role(
                    user_id=user_id, role_names=allowed_roles
                )

                if not is_authorized:
                    return HttpResponseForbidden(
                        "<h1>403 Forbidden</h1><p>You don't have the required role to view this page.</p>"
                    )

            except jwt.ExpiredSignatureError:
                return redirect("accounts:login")
            except (jwt.InvalidTokenError, UserAccount.DoesNotExist):
                return redirect("accounts:login")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
