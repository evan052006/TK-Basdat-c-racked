import uuid
from django.db import models


class UserAccount(models.Model):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_column="user_id"
    )
    username = models.CharField(max_length=100, unique=True, db_column="username")
    password = models.CharField(max_length=255, db_column="password")

    class Meta:
        db_table = "USER_ACCOUNT"
        managed = False

    # Ignore isActive to strictly follow schema requirements
    @property
    def is_active(self):
        return True

    # Tricking django to use purely our DB
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = False
