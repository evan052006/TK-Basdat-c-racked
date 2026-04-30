import jwt

from django.conf import settings
from .queries import accounts_db


def user_role_context(request):
    token = request.COOKIES.get("access_token")

    if not token:
        return {"user_role": "GUEST"}

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        active_role = payload.get("active_role")
        roles = [role["role_name"] for role in accounts_db.get_user_roles(user_id=user_id)]

        role = active_role if active_role in roles else (roles[0] if roles else "GUEST")
    except jwt.ExpiredSignatureError:
        return {"user_role": "GUEST"}
    except jwt.InvalidTokenError:
        return {"user_role": "GUEST"}
    except Exception:
        return {"user_role": "GUEST"}

    return {"user_role": role}
