import uuid
from django.db import models


class Role(models.Model):
    role_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_column="role_id"
    )
    role_name = models.CharField(max_length=50, unique=True, db_column="role_name")

    class Meta:
        db_table = "ROLE"
        managed = False


class UserAccount(models.Model):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_column="user_id"
    )
    username = models.CharField(max_length=100, unique=True, db_column="username")
    password = models.CharField(max_length=255, db_column="password")

    roles = models.ManyToManyField(Role, through="AccountRole", related_name="users")

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


class AccountRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column="role_id")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, db_column="user_id")

    class Meta:
        db_table = "ACCOUNT_ROLE"
        unique_together = (("user", "role"),)
        managed = False
