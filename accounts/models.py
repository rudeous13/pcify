from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer: {self.user.email}"


class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Staff: {self.user.email}"
