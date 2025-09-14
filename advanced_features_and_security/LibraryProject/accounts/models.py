from __future__ import annotations

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username: str, email: str | None = None, password: str | None = None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        Handles extra fields like date_of_birth and profile_photo.
        """
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str | None = None, password: str | None = None, **extra_fields):
        """
        Creates and saves a superuser. Ensures is_staff/is_superuser are True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, password=password, **extra_fields)


def user_profile_upload_path(instance: "User", filename: str) -> str:
    # uploads/avatars/user_<id>/<filename>
    return f"uploads/avatars/user_{instance.pk}/{filename}"


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Keeps Django's username authentication, adds:
    - date_of_birth (DateField, optional)
    - profile_photo (ImageField, optional)
    """
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to=user_profile_upload_path,
        null=True,
        blank=True
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.get_username()
