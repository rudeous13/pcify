from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Role, Staff


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_staff_for_superuser(sender, instance, created, **kwargs):
    """Attach Staff(Admin) profile only when a superuser is first created."""
    if not created or not instance.is_superuser:
        return

    admin_role, _ = Role.objects.get_or_create(role_name="Admin")
    Staff.objects.get_or_create(user=instance, defaults={"role": admin_role})
