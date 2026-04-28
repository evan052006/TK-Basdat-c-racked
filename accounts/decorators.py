import jwt
from functools import wraps
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import UserAccount


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

                # TODO turn this into pugsql query
                user = UserAccount.objects.prefetch_related("roles").get(
                    user_id=user_id
                )

                user_roles = set(user.roles.values_list("role_name", flat=True))
                required_roles = set(allowed_roles)

                if not user_roles.intersection(required_roles):
                    return HttpResponseForbidden(
                        "<h1>403 Forbidden</h1><p>You don't have the required role to view this page.</p>"
                    )

                request.user = user

            except jwt.ExpiredSignatureError:
                return redirect("login_page")
            except (jwt.InvalidTokenError, UserAccount.DoesNotExist):
                return redirect("login_page")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
