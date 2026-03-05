from django.contrib import admin
from .models import User, Role, Staff, Customer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "is_staff", "is_superuser")
    search_fields = ("email",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_name",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("role",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
