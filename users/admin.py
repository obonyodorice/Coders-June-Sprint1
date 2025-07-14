# your_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "first_name", "last_name", "user_type", "is_active")
    
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("user_type",)}),
    )
   
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("user_type",)}),
    )
