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

        role = accounts_db.get_user_role(user_id=user_id)
    except jwt.ExpiredSignatureError:
        return {"user_role": "GUEST"}
    except jwt.InvalidTokenError:
        return {"user_role": "GUEST"}

    return {"user_role": role}
