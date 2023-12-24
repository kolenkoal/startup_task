from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователей в системе для модели User."""

    def create_user(
            self,
            email,
            first_name,
            last_name,
            password=None,
            **extra_fields,
    ):
        """
        Создает и сохраняет пользователя с указанным email и паролем.

        Raises:
        - ValueError: Если email, имя или фамилия не указаны.
        """
        if not email:
            raise ValueError("Email должен быть указан.")
        if not first_name:
            raise ValueError("Имя должно быть указано.")
        if not last_name:
            raise ValueError("Фамилия должна быть указана.")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
            self,
            email,
            first_name,
            last_name,
            password=None,
            **extra_fields,
    ):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.

        Raises:
        - ValueError: Если email, имя или фамилия не указаны.
        """
        if not email:
            raise ValueError("Email должен быть указан.")
        if not first_name:
            raise ValueError("Имя должно быть указано.")
        if not last_name:
            raise ValueError("Фамилия должна быть указана.")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Пользователь в системе."""

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
